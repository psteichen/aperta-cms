from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from password_reset.views import recover, recover_done, reset, reset_done

from .views import home

# custom error views
handler400 = 'cms.errors.code400'
handler403 = 'cms.errors.code403'
handler404 = 'cms.errors.code404'
handler500 = 'cms.errors.code500'

urlpatterns = patterns('',
  url(r'^$', home, name='home'),

  #login stuff
  url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth.html'}, name='login'),
  url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
#  url(r'^chgpwd/$', 'django.contrib.auth.views.password_change', {'template_name': 'chgpwd.html', 'post_change_redirect': '/chgpwd-done/'}, name='chgpwd'),
#  url(r'^chgpwd-done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'done.html'}, name='chgpwd-done'),
  url(r'^pwd/change/', 'django.contrib.auth.views.password_change', {'template_name': 'pwd/change.html', 'post_change_redirect': '/pwd/change/done/'}, name='password_change'),
  url(r'^pwd/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'done.html'}, name='password_change_done'),
  url(r'^pwd/recover/$', recover, name='password_reset_recover'),
  url(r'^pwd/recover/(?P<signature>.+)/$', recover_done, name='password_reset_sent'),
  url(r'^pwd/reset/done/$', reset_done, name='password_reset_done'),
  url(r'^pwd/reset/(?P<token>[\w:-]+)/$', reset, name='password_reset_reset'),

  url(r'^attendance/', include('attendance.urls')),
  url(r'^locations/', include('locations.urls')),
  url(r'^upload/', include('upload.urls')),

  url(r'^meetings/', include('meetings.urls')),
  url(r'^members/', include('members.urls')),
  url(r'^finance/', include('finance.urls')),

  url(r'^events/', include('events.urls')),
  url(r'^web/', include('web.urls')),
#  url(r'^selling/', include('selling.urls')),
 
  url(r'^admin/', include(admin.site.urls)),
)
