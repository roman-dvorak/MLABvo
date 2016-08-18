from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import resolve_url

from django.template.loader import render_to_string



import warnings

from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import PBKDF2PasswordHasher, make_password, check_password
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


import datetime
from .models import AuthUser

from .MLABvo import _sql, getProjects 
from .MLABvo import * 


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    message = False
    if request.method == 'POST':
        print "post method"
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)   
        print user   

        if user is not None:
            auth.login(request, user)
            print "login OK"
            return HttpResponseRedirect('/')
        else:
            print "login ERR"
            message = "invalid loggin, try it again"

    cs = {'message': message}
    cs.update(csrf(request))
    return render(request, 'registration/login.html', cs)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)      

    if user is not None:
        auth.login(request, user)
        print "login OK"
        return HttpResponseRedirect('/')
    else:
        print "login ERR"
        return HttpResponseRedirect('/user/invalid')



def logout(request):
    auth_logout(request)
    return TemplateResponse(request, 'registration/logged_out.html')


def logout_then_login(request, login_url=None, current_app=None, extra_context=None):
    """
    Logs out the user if they are logged in. Then redirects to the log-in page.
    """
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = resolve_url(login_url)
    return logout(request, login_url, current_app=current_app, extra_context=extra_context)


def redirect_to_login(next, login_url=None,
                      redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirects the user to the login page, passing the given 'next' page
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))


# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': _('Password reset sent'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
def register(request):
    context = RequestContext(request)
    registered = False
    message = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        first_name= request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username  = request.POST.get('username', '')
        email     = request.POST.get('email', '')
        password  = make_password(request.POST.get('password', ''))

        print first_name, last_name, username, email, password
        try:
            if True: # TODO: zkontrolovat spravnost dat
                au = AuthUser(username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                date_joined = datetime.datetime.now(),
                last_login = datetime.datetime.now())
                au.save()

                registered = True
                htlm_mail = render_to_string('registration/email.html', {'first_name': first_name, 'last_name': last_name, 'username': username}, context)                
                msg = EmailMultiAlternatives('[MLABvo] new registration', "Hi, tenhle mail ma html cast, zkus otevrit tu...", 'rdvorakdvroak@gmail.com', [email])
                msg.attach_alternative(htlm_mail, "text/html")
                msg.send()


            else:
                print user_form.errors, profile_form.errors

        except Exception, e:
            if e[0] == 1062:
                message = "User exist"
            else:
                message = "Error" + repr(e[0])

    # Render the template depending on the context.
    return render_to_response('registration/register.html', {'registered': registered, 'message': message}, context)





@login_required
def profile(request, username = None):
    return render_to_response('registration/setting.html')


@login_required
def adminBase(request, type = None, project = None):
    if project:
        context = {'projects': getProjects(),'project_selected': getProjectByName(project), 'tables': getProjectTables(project)}
        return render_to_response('registration/setting_project.html', context)

    elif type == None:
        context = {'projects': getProjects()}
        return render_to_response('registration/setting_home.html', context)
