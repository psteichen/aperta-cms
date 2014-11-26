from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from attendance.forms import ModifyAttendanceForm

from .forms import ListMeetingsForm, ModifyMeetingForm
from .views import ModifyMeetingWizard, show_attendance_form
from .views import index, add, send, list_all, list

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

  url(r'^add/$', add, name='add'),
  url(r'^send/$', send, name='send'),

  url(r'^modify/(?P<meeting_num>.+?)/$', modify_meeting_wrapper, name='modify'),

  url(r'^list_all/$', list_all, name='list_all'),
  url(r'^list/(?P<meeting_num>.+?)/$', list, name='list'),

)
