from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login, password_change, password_change_done
from django.contrib import admin
admin.autodiscover()

from .views import home

# custom error views
handler400 = 'cms.errors.code400'
handler403 = 'cms.errors.code403'
handler404 = 'cms.errors.code404'
handler500 = 'cms.errors.code500'

urlpatterns = [
  url(r'^$', home, name='home'),

  #login stuff
  url(r'^login/$', login, {'template_name': 'auth.html'}, name='login'),
  url(r'^logout/$', logout_then_login, name='logout'),
  url(r'^chgpwd/$', password_change, {'template_name': 'chgpwd.html', 'post_change_redirect': '/chgpwd-done/'}, name='chgpwd'),
  url(r'^chgpwd-done/$', password_change_done, {'template_name': 'done.html'}, name='chgpwd-done'),

  url(r'^attendance/', include('attendance.urls')),
  url(r'^locations/', include('locations.urls')),

  url(r'^meetings/', include('meetings.urls')),
  url(r'^members/', include('members.urls')),
  url(r'^upload/', include('upload.urls')),
  url(r'^finance/', include('finance.urls')),

  url(r'^events/', include('events.urls')),
  url(r'^upload/', include('upload.urls')),
 
  url(r'^setup/', include('setup.urls')),
  url(r'^admin/', include(admin.site.urls)),
]
