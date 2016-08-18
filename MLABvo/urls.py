from django.conf.urls import patterns, include, url
from django.contrib import admin
from .models import *

admin.autodiscover()
admin.site.site_header = 'My Site Admin'
admin.site.register(VoFileindex)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MLABvo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^$', 'MLABvo.home.home', name='home'),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/$', 'MLABvo.user.adminBase', name='admin'),
    url(r'^admin/project/(?P<project>[\w-]+)$', 'MLABvo.user.adminBase', name='admin'),
    url(r'^project/(?P<project>[\w-]+)$', 'MLABvo.user.adminBase', name='admin'),
    url(r'^table/(?P<table>[\w-]+)$', 'MLABvo.user.adminBase', name='admin'),
    url(r'^login/$', 'MLABvo.user.login', name='login'),
    url(r'^user/login/$', 'MLABvo.user.login'),
    url(r'^user/auth_view/', 'MLABvo.user.auth_view'),
    url(r'^user/logout/$', 'MLABvo.user.logout', name='user_logout'),
    url(r'^user/login_invalid/$', 'MLABvo.user.invalid'),
    url(r'^registration/$', 'MLABvo.user.register', name='registation'),
    url(r'^user/register/$', 'MLABvo.user.register'),
    url(r'^user/register_succes/$', 'MLABvo.user.register_succes', name = 'register_succes'),
    url(r'^user/(?P<username>[\w-]+)$', 'MLABvo.user.profile'),
    url(r'^tap/sync$', 'MLABvo.api.tap', name = 'tapSync'),
    url(r'^api/upload/(?P<project>[\w-]+)/$', 'MLABvo.api.upload', name = 'upload'),
    url(r'^sync$', 'MLABvo.api.sync', name = 'sync'),
    url(r'^tap/$(?P<path>.*)$', 'MLABvo.api.tap', name = 'tap'),
)
