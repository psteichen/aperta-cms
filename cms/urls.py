from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import home

urlpatterns = patterns('',
  url(r'^$', home, name='home'),

  #login stuff
  url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth.html'}, name='login'),
  url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
  url(r'^chgpwd/$', 'django.contrib.auth.views.password_change', {'template_name': 'chgpwd.html', 'post_change_redirect': '/chgpwd-done/'}, name='chgpwd'),
  url(r'^chgpwd-done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'done/chgpwd.html'}, name='chgpwd-done'),

  url(r'^members/', include('members.urls')),

  url(r'^attendance/', include('attendance.urls')),

  url(r'^locations/', include('locations.urls')),

  url(r'^meetings/', include('meetings.urls')),

  url(r'^events/', include('events.urls')),

  url(r'^selling/', include('selling.urls')),

#  url(r'^webcontent/', include('webcontent.urls')),

  url(r'^admin/', include(admin.site.urls)),
)
