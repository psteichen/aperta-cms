from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from attendance.forms import ModifyAttendanceForm
from locations.forms import LocationForm

from .views import index, wouldbe, send, list_all, list

from .forms import AddMeetingForm
from .views import AddMeetingWizard, show_location_form

from .forms import ModifyMeetingForm
from .views import ModifyMeetingWizard, show_attendance_form

# add meeting wizard #
#forms
add_meeting_forms = [
        ('meeting'	, AddMeetingForm),
        ('location'	, LocationForm),
]
#condition dict
add_meeting_condition_dict = {
	'location'	: show_location_form,
}
#view
add_meeting_wizard = AddMeetingWizard.as_view(add_meeting_forms, condition_dict=add_meeting_condition_dict)
#wrapper with specific permissions
add_meeting_wrapper = permission_required('cms.COMM',raise_exception=True)(add_meeting_wizard)

# modify meeting wizard #
#forms
modify_meeting_forms = [
        ('meeting'	, ModifyMeetingForm),
        ('attendance'	, ModifyAttendanceForm),
]
#condition dict
modify_meeting_condition_dict = {
	'attendance'	: show_attendance_form,
}
#view
modify_meeting_wizard = ModifyMeetingWizard.as_view(modify_meeting_forms, condition_dict=modify_meeting_condition_dict)
#wrapper with specific permissions
modify_meeting_wrapper = permission_required('cms.BOARD',raise_exception=True)(modify_meeting_wizard)

urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/$', add_meeting_wrapper, name='add'),
  url(r'^wouldbe/(?P<meeting_num>.+?)/(?P<attendance_hash>.+?)/$', wouldbe, name='wouldbe'),
  url(r'^send/$', send, name='send'),

  url(r'^modify/(?P<meeting_num>.+?)/$', modify_meeting_wrapper, name='modify'),

  url(r'^list_all/$', list_all, name='list_all'),
  url(r'^list/(?P<meeting_num>.+?)/$', list, name='list'),

)
