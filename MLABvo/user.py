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



@sensitive_post_parameters()
def register(request):
    context = RequestContext(request)
    registered = False
    message = False

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
