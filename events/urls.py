from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from attendance.forms import ModifyAttendanceForm

from .views import index, send, list_all, list

from locations.forms import LocationForm
from .forms import AddEventForm
from .views import AddEventWizard, show_location_form

from .forms import ModifyEventForm
from .views import ModifyEventWizard, show_attendance_form

# add event wizard #
#forms
add_event_forms = [
        ('event'	, AddEventForm),
        ('location'	, LocationForm),
]
#condition dict
add_event_condition_dict = {
	'location'	: show_location_form,
}
#view
add_event_wizard = AddEventWizard.as_view(add_event_forms, condition_dict=add_event_condition_dict)
#wrapper with specific permissions
add_event_wrapper = permission_required('cms.COMM',raise_exception=True)(add_event_wizard)

# modify event wizard #
#forms
modify_event_forms = [
        ('event'	, ModifyEventForm),
        ('attendance'	, ModifyAttendanceForm),
]
#condition dict
modify_event_condition_dict = {
	'attendance'	: show_attendance_form,
}
#view
modify_event_wizard = ModifyEventWizard.as_view(modify_event_forms, condition_dict=modify_event_condition_dict)
#wrapper with specific permissions
modify_event_wrapper = permission_required('cms.COMM',raise_exception=True)(modify_event_wizard)

urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/$', add_event_wrapper, name='add'),
  url(r'^send/$', send, name='send'),

  url(r'^modify/(?P<event_id>.+?)/$', modify_event_wrapper, name='modify'),

  url(r'^list_all/$', list_all, name='list_all'),
  url(r'^list/(?P<event_id>.+?)/$', list, name='list'),
)
