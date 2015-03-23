from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from .forms import ListEventsForm, ModifyEventForm
from .views import ModifyEventWizard
from .views import index, add, send, list_all, list

# modify event wizard #
#forms
modify_event_forms = [
        ('list'         , ListEventsForm),
        ('meeting'	, ModifyEventForm),
]
#view
modify_event_wizard = ModifyEventWizard.as_view(modify_event_forms)
#wrapper with specific permissions
modify_event_wrapper = permission_required('cms.COMM',raise_exception=True)(modify_event_wizard)

urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/$', add, name='add'),
  url(r'^send/$', send, name='send'),
  url(r'^modify/$', modify_event_wrapper, name='modify'),
  url(r'^list_all/$', list_all, name='list_all'),
  url(r'^list/(?P<event_id>.+?)/$', list, name='list'),
)
