from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from attendance.forms import ModifyAttendanceForm

from .forms import ListMeetingsForm, ModifyMeetingForm
from .views import ModifyMeetingWizard, show_attendance_form
from .views import list, add, send, invite, details, report

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
  url(r'^$', list, name='list'),
  url(r'^list/(?P<meeting_num>.+?)/$', details, name='details'),
  url(r'^invite/(?P<meeting_num>.+?)/(?P<member_id>.+?)/$', invite, name='invite'),

  url(r'^add/$', add, name='add'),
  url(r'^send/(?P<meeting_num>.+?)/$', send, name='send'),
  url(r'^modify/(?P<meeting_num>.+?)/$', modify_meeting_wrapper, name='modify'),
  url(r'^report/(?P<meeting_num>.+?)/$', report, name='report'),
)
