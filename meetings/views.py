#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from cms.functions import notify_by_email, show_form

from events.models import Event
from members.models import Member
from members.functions import get_active_members, gen_member_fullname
from attendance.functions import gen_invitation_message
from attendance.models import Meeting_Attendance

from .functions import gen_meeting_overview, gen_meeting_initial, gen_current_attendance
from .models import Meeting, Invitation
from .forms import  MeetingForm, ListMeetingsForm
from .tables  import MeetingTable, MgmtMeetingTable


#################
# MEETING VIEWS #
#################

# list #
########
@permission_required('cms.MEMBER',raise_exception=True)
def list(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('meetings','/meetings/'),
               ) )

  table = MeetingTable(Meeting.objects.all().order_by('-num'))
  if r.user.has_perm('cms.BOARD'):
    table = MgmtMeetingTable(Meeting.objects.all().order_by('-num'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['template'], {
                   'title': settings.TEMPLATE_CONTENT['meetings']['title'],
                   'actions': settings.TEMPLATE_CONTENT['meetings']['actions'],
                   'table': table,
                })


# add #
#######
@permission_required('cms.BOARD',raise_exception=True)
def add(r):
  r.breadcrumbs( ( 	
			('home','/'),
                   	('meetings','/meetings/'),
                   	('add meeting','/meetings/add/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['template']

    mf = MeetingForm(r.POST)
    if mf.is_valid():
      Mt = mf.save(commit=False)
      Mt.save()
      
      I = Invitation(meeting=Mt,message=mf.cleaned_data['additional_message'])
      send = mf.cleaned_data['send']
      if send:
        email_error = { 'ok': True, 'who': (), }
        for m in get_active_members():
   
          #invitation email with "YES/NO button"
          subject = settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
          invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,m) + mf.cleaned_data['additional_message']
          message_content = {
            'FULLNAME'    : gen_member_fullname(m),
            'MESSAGE'     : invitation_message,
          }
          #send email
          ok=notify_by_email(r.user.email,m.email,subject,message_content)
          if not ok: 
            email_error['ok']=False
            email_error['who'].add(m.email)

        # error in email -> show error messages
        if not email_error['ok']:
          I.sent = datetime.now()
          I.save()
          return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                })

      # all fine -> done
      I.save()
      invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,Member(user=r.user)) + mf.cleaned_data['additional_message']
      return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['meetings']['add']['done']['message'] % { 'email': invitation_message, 'list': ' ; '.join([gen_member_fullname(m) for m in get_active_members()]), },
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MeetingForm()
    try:
      latest = Meeting.objects.values().latest('num')
      next_num = latest['num'] + 1
      form = MeetingForm(initial={ 'title': str(next_num) + '. réunion statutaire', 'num': next_num, })
    except Meeting.DoesNotExist:
      pass
    return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['meetings']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['add']['submit'],
                'form': form,
                })

# send #
########
@permission_required('cms.BOARD',raise_exception=True)
def send(r, meeting_num):
  r.breadcrumbs( ( 
			('home','/'),
                   	('meetings','/meetings/'),
                   	('send meeting invitations','/meetings/send/'),
               ) )

  e_template =  settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['template']

  Mt = Meeting.objects.get(num=meeting_num)
  I = Invitation.objects.get(meeting=Mt)

  title = settings.TEMPLATE_CONTENT['meetings']['send']['done']['title'] % unicode(Mt.title)
      
  email_error = { 'ok': True, 'who': (), }
  for m in get_active_members():
    #invitation email with "YES/NO button"
    subject = settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
    invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,m)
    message_content = {
        'FULLNAME'    : gen_member_fullname(m),
        'MESSAGE'     : invitation_message + I.message,
    }
    #send email
    ok=notify_by_email(r.user.email,m.email,subject,message_content)
    if not ok: 
      email_error['ok']=False
      email_error['who'].add(m.email)

  # error in email -> show error messages
  if not email_error['ok']:
    return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['done']['template'], {
                	'title': title, 
       	        	'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                  })

  # all fine -> done
  else:
    I.sent = datetime.now()
    I.save()
    return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['meetings']['send']['done']['message'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                  })


# details #
############
@login_required
def details(r, meeting_num):
  r.breadcrumbs( ( 
			('home','/'),
                   	('meetings','/meetings/'),
                   	('details for meeting n. '+meeting_num,'/meetings/list/'+meeting_num+'/'),
               ) )

  meeting = Meeting.objects.get(num=meeting_num)
  title = settings.TEMPLATE_CONTENT['meetings']['details']['title'] % { 'meeting' : meeting.title, }
  message = gen_meeting_overview(settings.TEMPLATE_CONTENT['meetings']['details']['overview']['template'],meeting)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['details']['template'], {
                   'title': title,
                   'message': message,
                })


# modify #
##########

#modify helper functions
def show_attendance_form(wizard):
  return show_form(wizard,'meeting','attendance',True)

#modify formwizard
class ModifyMeetingWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyMeetingWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('modify a meeting','/meetings/modify/'),
                            ) )

    if self.steps.current != None:
      title = u'réunion'
      meeting_num = self.kwargs['meeting_num']
      title = Meeting.objects.get(pk=meeting_num).title
      context.update({'title': settings.TEMPLATE_CONTENT['meetings']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['meetings']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['meetings']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['meetings']['modify'][self.steps.current]['title'] % { 'meeting': title, } })
      context.update({'next': settings.TEMPLATE_CONTENT['meetings']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyMeetingWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    meeting_num = self.kwargs['meeting_num']
    M = Meeting.objects.get(pk=meeting_num)

    if step == 'meeting':
      form.initial = gen_meeting_initial(M)
      form.instance = M

    if step == 'attendance':
      form.initial = gen_current_attendance(M)

    return form

  def done(self, form_list, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('modify a meeting','/meetings/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['template']

    M = None
    mf = form_dict['meeting']
    if mf.is_valid():
      M = mf.save()

      attendance = mf.cleaned_data['attendance']
      if attendance == True: 
        af = form_dict['attendance']
        if af.is_valid() and af.has_changed():
          s_initial = af.initial['subscribed']
          s_changed = af.cleaned_data['subscribed']
          for s in s_changed:
            try:
              Meeting_Attendance(meeting=M,member=s,timestamp=datetime.now(),present=True).save()
            except: pass
#          s_diff = set(s_initial) ^ set(s_changed)
#          for s_d in s_diff:
#            try:
#              Meeting_Attendance.objects.get(meeting=M,member=s_d).delete()
#            except:
#              pass

          e_initial = af.initial['excused']
          e_changed = af.cleaned_data['excused']
          for e in e_changed:
            try:
              Meeting_Attendance(meeting=M,member=e,timestamp=datetime.now(),present=False).save()
            except: pass
#          e_diff = set(e_initial) ^ set(e_changed)
#          for e_d in e_diff:
#            try:
#              Meeting_Attendance.objects.get(meeting=M,member=e_d).delete()
#            except:
#              pass

    title = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['title'] % M

    return render(self.request, template, {
                        'title': title,
                 })

