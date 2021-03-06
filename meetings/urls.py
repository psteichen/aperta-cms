from django.conf.urls import include, url

from .views import list, add, modify, send, invite, details, report, print, register

urlpatterns = [
  url(r'^$', list, name='list'),
  url(r'^list/(?P<meeting_num>.+?)/$', details, name='details'),
  url(r'^print/(?P<meeting_num>.+?)/$', print, name='print'),
  url(r'^invite/(?P<meeting_num>.+?)/(?P<member_id>.+?)/$', invite, name='invite'),

#below urls need permissions
  url(r'^add/$', add, name='add'),
  url(r'^send/(?P<meeting_num>.+?)/$', send, name='send'),
  url(r'^modify/(?P<meeting_num>.+?)/$', modify, name='modify'),
  url(r'^report/(?P<meeting_num>.+?)/$', report, name='report'),
  url(r'^register/(?P<meeting_num>.+?)/(?P<mode>.+?)/$', register, name='register'),

]
