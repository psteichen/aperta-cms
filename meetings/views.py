#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_tables2 import RequestConfig

from cms.functions import notify_by_email, show_form

from events.models import Event
from members.models import Member
from members.functions import get_active_members, gen_member_fullname
from attendance.functions import gen_invitation_message
from attendance.models import Meeting_Attendance

from .functions import get_next_meeting_num, gen_meeting_overview, gen_meeting_initial, gen_current_attendance
from .models import Meeting, Invitation
from .forms import WouldBeForm, ListMeetingsForm
from .tables  import MeetingTable


# index #
#########
@login_required
def index(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
               ) )

  return render(r, settings.TEMPLATE_CONTENT['meetings']['template'], {
                   'title': settings.TEMPLATE_CONTENT['meetings']['title'],
                   'actions': settings.TEMPLATE_CONTENT['meetings']['actions'],
               })


#################
# MEETING VIEWS #
#################

# add #
#######

#add helper functions
def show_location_form(wizard):
  return show_form(wizard,'meeting','new_location',True)

#add formwizard
class AddMeetingWizard(SessionWizardView):

  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(AddMeetingWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('add a meeting','/meetings/add/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['meetings']['add']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['meetings']['add']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['meetings']['add']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['meetings']['add'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['meetings']['add'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(AddMeetingWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'meeting':
#HERE (check with old code how to add num and title correctly)
#      form.fields['num'].field = get_next_meeting_num()
      form.fields['title'].field =  u'%i. Réunion Statuaire' % get_next_meeting_num()

    return form

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('add a meeting','/meetings/add/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['meetings']['add']['done']['template']
    e_template =  settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['template']
    error_message = ''

    M = L = None
    mf = form_dict['meeting']
    location = mf.cleaned_data['new_location']
    if location: 
      lf = form_dict['location']
      if lf.is_valid():
        L = lf.save()

    if mf.is_valid():
      M = mf.save()

      I = Invitation(meeting=M,message=mf.cleaned_data['additional_message'])

      send = mf.cleaned_data['send']
      if send:
        email_error = { 'ok': True, 'who': (), }
        for m in get_active_members():
   
          #invitation email with "YES/NO button"
          subject = settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['subject'] % { 'title': unicode(M.title) }
          invitation_message = gen_invitation_message(e_template,M,Event.MEET,m) + mf.cleaned_data['additional_message']
          message_content = {
            'FULLNAME'    : gen_member_fullname(m),
            'MESSAGE'     : invitation_message,
          }
          #send email
          ok=notify_by_email(self.request.user.email,m.email,subject,message_content)
          if not ok: 
            email_error['ok']=False
            email_error['who'].add(m.email)

        # error in email
        if not email_error['ok']:
          I.sent = datetime.now()
          error_message = settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),

#HERE (somehow this save does not work)
      I.save()

      title = settings.TEMPLATE_CONTENT['meetings']['add']['done']['title']
      invitation_message = gen_invitation_message(e_template,M,Event.MEET,Member(user=self.request.user)) + mf.cleaned_data['additional_message']
      message = settings.TEMPLATE_CONTENT['meetings']['add']['done']['message'] % { 'email': invitation_message, 'list': ' ; '.join([gen_member_fullname(m) for m in get_active_members()]) },

      return render(self.request, template, {
                        'title': title,
     		        'message': message,
                	'error_message': error_message,
                   })

# wouldbe #
###########
def wouldbe(r,meeting_num, attendance_hash):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('invite a wouldbe for meeting n. '+meeting_num,'/meetings/wouldb/'+meeting_num+'/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['email']['template']

    wf = WouldBeForm(r.POST)
    if wf.is_valid():
      W = wf.save(commit=False)
      W.status = Member.WBE
      W.start_date = date.today()
      W.save()

      Mt = Meeting.objects.get(num=meeting_num)
      additional_message = Invitation.objects.get(meeting=Mt).message or ''

      title = settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['title']
      subject = settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['email']['subject'] % { 'title': unicode(Mt.title) }

      # cycle though members to identify the sponsor based on attendance_hash
      for m in get_active_members():
        if gen_hash(Mt,m.email) == attendance_hash:
          invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,W,m) + additional_message
          message_content = {
            'FULLNAME'    : gen_member_fullname(W),
            'MESSAGE'     : invitation_message
          }
  
          #send email
          ok=notify_by_email(False,W.email,subject,message_content,m.email)
          if not ok: 
            # error in email -> show error messages
            W.delete()
            return render(r, settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['template'], {
				'title': title, 
            		        'error_message': settings.TEMPLATE_CONTENT['error']['email'],
			 })
  
      return render(r, settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['template'], {
  	                'title': title, 
          	        'message': settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['message'] % { 'name': gen_member_fullname(W), 'meeting': unicode(Mt.title) }
                   })
  
    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['wouldbe']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['wouldbe']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in wf.errors]),
                })
  # no post yet -> empty form
  else:
    form = WouldBeForm()
    return render(r, settings.TEMPLATE_CONTENT['meetings']['wouldbe']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['wouldbe']['title'],
                'desc': settings.TEMPLATE_CONTENT['meetings']['wouldbe']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['wouldbe']['submit'],
                'form': form,
                })
 

# send #
########
@login_required
def send(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('send meeting invitations','/meetings/send/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['template']

    lmf = ListMeetingsForm(r.POST)
    if lmf.is_valid():
      Mt = lmf.cleaned_data['meetings']

      title = settings.TEMPLATE_CONTENT['meetings']['send']['done']['title'] % unicode(Mt.title)
      
      email_error = { 'ok': True, 'who': (), }
      for m in get_active_members():
   
        #invitation email with "YES/NO button"
        subject = settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
        invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,m)
        message_content = {
          'FULLNAME'    : gen_member_fullname(m),
          'MESSAGE'     : invitation_message + mf.cleaned_data['additional_message'],
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
        return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['meetings']['send']['done']['message'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                      })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['send']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = ListMeetingsForm()
    return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['send']['title'],
                'desc': settings.TEMPLATE_CONTENT['meetings']['send']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['send']['submit'],
                'form': form,
                })
 

# list #
#########
@login_required
def list(r, meeting_num):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('list meeting n. '+meeting_num,'/meetings/list/'+meeting_num+'/'),
               ) )

  meeting = Meeting.objects.get(num=meeting_num)
  title = settings.TEMPLATE_CONTENT['meetings']['list']['title'] % { 'meeting' : meeting.title, }
  message = gen_meeting_overview(settings.TEMPLATE_CONTENT['meetings']['list']['overview']['template'],meeting)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['list']['template'], {
                   'title': title,
                   'message': message,
                })

# list_all #
############
@login_required
def list_all(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('list meetings','/meetings/list_all/'),
               ) )

  table = MeetingTable(Meeting.objects.all().order_by('-num'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['list_all']['template'], {
                   'title': settings.TEMPLATE_CONTENT['meetings']['list_all']['title'],
                   'desc': settings.TEMPLATE_CONTENT['meetings']['list_all']['desc'],
                   'table': table,
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
          for s in af.cleaned_data['subscribed']:
            try:
              Meeting_Attendance(meeting=M,member=s,timestamp=datetime.now(),present=True).save()
            except:
              pass
          for e in af.cleaned_data['excused']:
            try:
              Meeting_Attendance(meeting=M,member=e,timestamp=datetime.now(),present=False).save()
            except:
              pass

    title = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['title'] % M

    return render(self.request, template, {
                        'title': title,
                 })

