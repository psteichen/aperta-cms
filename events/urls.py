from django.conf.urls import include, url

from .views import list, add, send, details, modify, register#, photos

urlpatterns = [
  url(r'^$', list, name='list'),
  url(r'^list/(?P<event_id>.+?)/$', details, name='details'),
  url(r'^reg/(?P<event_hash>.+?)/$', register, name='register'),

#below urls need permissions
  url(r'^add/$', add, name='add'),
  url(r'^send/(?P<event_id>.+?)/$', send, name='send'),
  url(r'^modify/(?P<event_id>.+?)/$', modify, name='modify'),
#  url(r'^photos/(?P<event_id>.+?)/$', photos, name='photos'),
]
