#
# coding=utf-8
#

from django.conf.urls import include, url
#from django.contrib.auth.views import login, logout_then_login, password_change, password_change_done, password_reset, password_reset_done, password_reset_confrim, password_reset_complete
from django.contrib import admin
admin.autodiscover()

from .views import home

# custom error views
handler400 = 'cms.errors.code400'
handler403 = 'cms.errors.code403'
handler404 = 'cms.errors.code404'
handler500 = 'cms.errors.code500'

urlpatterns = [

  #auth stuff
  url('^', include('django.contrib.auth.urls')),
  #this creates the following urls patterns:
  # ^login/$ [name='login']
  # ^logout/$ [name='logout']
  # ^password_change/$ [name='password_change']
  # ^password_change/done/$ [name='password_change_done']
  # ^password_reset/$ [name='password_reset']
  # ^password_reset/done/$ [name='password_reset_done']
  # ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
  # ^reset/done/$ [name='password_reset_complete'] 

  url(r'^$', home, name='home'),

  url(r'^attendance/', include('attendance.urls')),
  url(r'^members/', include('members.urls')),
  url(r'^meetings/', include('meetings.urls')),
  url(r'^events/', include('events.urls')),
  url(r'^upload/', include('upload.urls')),
  url(r'^locations/', include('locations.urls')),
  url(r'^finance/', include('finance.urls')),

  url(r'^setup/', include('setup.urls')),

  url(r'^admin/', include(admin.site.urls)),
]
