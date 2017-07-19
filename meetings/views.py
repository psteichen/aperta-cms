#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig

from cms.functions import notify_by_email, genIcal, show_form, visualiseDateTime

from events.models import Event
from members.models import Member
from members.functions import get_active_members, gen_member_fullname
from attendance.functions import gen_attendance_hashes, gen_invitation_message
from attendance.models import Meeting_Attendance

from .functions import gen_meeting_overview, gen_meeting_initial, gen_current_attendance, gen_report_message, gen_invitee_message, gen_meeting_listing
from .models import Meeting, Invitation
from .forms import  MeetingForm, ModifyMeetingForm, MeetingReportForm, InviteeFormSet
from .tables  import MeetingTable, MgmtMeetingTable, MeetingMixin, MeetingListingTable


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
                   'desc': settings.TEMPLATE_CONTENT['meetings']['desc'],
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
    done_message = ''

    mf = MeetingForm(r.POST,r.FILES)
    if mf.is_valid():
      Mt = mf.save(commit=False)
      Mt.save()
      
      user_member = Member.objects.get(user=r.user)
      e_subject = settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['subject'] % { 'title': unicode(Mt.title) }

      if r.FILES:
        I = Invitation(meeting=Mt,message=mf.cleaned_data['additional_message'],attachement=r.FILES['attachement'])
      else:
        I = Invitation(meeting=Mt,message=mf.cleaned_data['additional_message'])
      I.save()

      # all fine -> done
      I.save()
      return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['meetings']['add']['done']['message'] % { 'email': done_message, 'attachement': I.attachement, 'list': ' ; '.join([gen_member_fullname(m) for m in get_active_members()]), },
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
      
  email_error = { 'ok': True, 'who': [], }
  for m in get_active_members():
    #invitation email with "YES/NO button"
    subject = settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
    invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,m)
    message_content = {
        'FULLNAME'    : gen_member_fullname(m),
        'MESSAGE'     : invitation_message + I.message,
    }

    #generate ical invite
    invite = genIcal(Mt)

    #send email
    try: #with attachement
      ok=notify_by_email(settings.EMAILS['sender']['default'],m.email,subject,message_content,False,[invite,settings.MEDIA_ROOT + unicode(I.attachement)])
    except: #no attachement
      ok=notify_by_email(settings.EMAILS['sender']['default'],m.email,subject,message_content,False,invite)
     
    if not ok: 
      email_error['ok']=False
      email_error['who'].append(m.email)

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


# invite #
##########
#@permission_required('cms.MEMBER',raise_exception=True)
def invite(r, meeting_num, member_id):

  Mt = M = None
  if meeting_num:
    Mt = Meeting.objects.get(pk=meeting_num)
    if member_id:
      M = Member.objects.get(pk=member_id)
  else:
    return render(r, settings.TEMPLATE_CONTENT['meetings']['invite']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['invite']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'],
                })

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['invite']['done']['email']['template']

    ifs = InviteeFormSet(r.POST)
    if ifs.is_valid():
      invitees = []

      I = Invitation.objects.get(meeting=Mt)
      invitation_message = gen_invitee_message(e_template,Mt,M)
      try: invitation_message += I.additional_message
      except: pass
      email_error = { 'ok': True, 'who': [], }
      for i in ifs:
        Iv = i.save(commit=False)
        Iv.meeting = Mt
        Iv.member = M
        if Iv.email:
          Iv.save()
      
          #invitation email for invitee(s)
          subject = settings.TEMPLATE_CONTENT['meetings']['invite']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
          message_content = {
            'FULLNAME'    : gen_member_fullname(Iv),
            'MESSAGE'     : invitation_message,
          }
          #send email
#no need to add attachement for invitees
#          try:
#            ok=notify_by_email(settings.EMAILS['sender']['default'],Iv.email,subject,message_content,False,settings.MEDIA_ROOT + unicode(I.attachement))
#          except:
          ok=notify_by_email(settings.EMAILS['sender']['default'],Iv.email,subject,message_content)
          if not ok:
            email_error['ok']=False
            email_error['who'].append(Iv.email)

          # all fine -> save Invitee
          invitees.append(Iv)

      # error in email -> show error messages
      if not email_error['ok']:
        return render(r, settings.TEMPLATE_CONTENT['meetings']['invite']['done']['template'], {
              'title': settings.TEMPLATE_CONTENT['meetings']['invite']['done']['title'], 
              'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
              })

      # all fine -> done
      I.sent = timezone.now()
      I.save()
      return render(r, settings.TEMPLATE_CONTENT['meetings']['invite']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['invite']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['meetings']['invite']['done']['message'] % { 'email': invitation_message, 'attachement': I.attachement, 'list': ' ; '.join([gen_member_fullname(i) for i in invitees]), },
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['invite']['done']['template'], {
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([str(e) for e in ifs.errors]),
                })
  # no post yet -> empty form
  else:
    return render(r, settings.TEMPLATE_CONTENT['meetings']['invite']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['invite']['title'] + unicode(Mt),
                'desc': settings.TEMPLATE_CONTENT['meetings']['invite']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['invite']['submit'],
                'form': InviteeFormSet(),
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


# listing #
###########
@login_required
def listing(r, meeting_num):
  r.breadcrumbs( (
                        ('home','/'),
                        ('meetings','/meetings/'),
                        ('listing for meeting n. '+meeting_num,'/meetings/listing/'+meeting_num+'/'),
               ) )

  meeting = Meeting.objects.get(num=meeting_num)
  title = settings.TEMPLATE_CONTENT['meetings']['listing']['title'] % { 'meeting' : meeting.title, }
  message = gen_meeting_listing(settings.TEMPLATE_CONTENT['meetings']['listing']['content']['template'],meeting)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['listing']['template'], {
                   'title': title,
                   'message': message,
                })


# modify #
##########
@permission_required('cms.BOARD',raise_exception=True)
def modify(r,meeting_num):
  r.breadcrumbs( ( 	
			('home','/'),
                   	('meetings','/meetings/'),
                   	('modify meeting','/meetings/modify/'+meeting_num+'/'),
               ) )

  Mt = Meeting.objects.get(pk=meeting_num)
  template	= settings.TEMPLATE_CONTENT['meetings']['modify']['template']
  title 	= settings.TEMPLATE_CONTENT['meetings']['modify']['title'].format(meeting=unicode(Mt))
  desc 		= settings.TEMPLATE_CONTENT['meetings']['modify']['desc']
  submit	= settings.TEMPLATE_CONTENT['meetings']['modify']['submit']

  done_template	= settings.TEMPLATE_CONTENT['meetings']['modify']['done']['template']
  done_title 	= settings.TEMPLATE_CONTENT['meetings']['modify']['done']['title'].format(meeting=unicode(Mt))
  done_message	= settings.TEMPLATE_CONTENT['meetings']['modify']['done']['message'].format(meeting=unicode(Mt))

  if r.POST:
    done_message = ''

    mf = ModifyMeetingForm(r.POST,instance=Mt)
    if mf.is_valid():
      Mt = mf.save(commit=False)
      Mt.save()
      
      # all fine -> done
      return render(r, done_template, {
                'title'		: done_title, 
                'message'	: done_message,
                })

    # form not valid -> error
    else:
      return render(r, done_template, {
                'title'		: done_title, 
                'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = ModifyMeetingForm()
    form.initial = gen_meeting_initial(Mt)
    form.instance = Mt
    return render(r, template, {
                'title'	: title,
                'desc'	: desc,
                'submit': submit,
                'form'	: form,
                })


# report #
##########
@permission_required('cms.BOARD',raise_exception=True)
def report(r, meeting_num):
  r.breadcrumbs( ( 	
			('home','/'),
                   	('meetings','/meetings/'),
               ) )

  Mt = Meeting.objects.get(num=meeting_num)

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['report']['done']['email']['template']

    mrf = MeetingReportForm(r.POST, r.FILES)
    if mrf.is_valid():
      Mt.report = mrf.cleaned_data['report']
      Mt.save()

      send = mrf.cleaned_data['send']
      if send:
        email_error = { 'ok': True, 'who': [], }
        for m in get_active_members():
   
          #notifiation per email for new report
          subject = settings.TEMPLATE_CONTENT['meetings']['report']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
          message_content = {
            'FULLNAME'    : gen_member_fullname(m),
            'MESSAGE'     : gen_report_message(e_template,Mt,m),
          }
          attachement = settings.MEDIA_ROOT + unicode(Mt.report)
          #send email
          ok=notify_by_email(settings.EMAILS['sender']['default'],m.email,subject,message_content,False,attachement)
          if not ok: 
            email_error['ok']=False
            email_error['who'].append(m.email)

        # error in email -> show error messages
        if not email_error['ok']:
          return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                })
        else:
          # done -> with sending
          return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
				'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title_send'], 
                		'message': settings.TEMPLATE_CONTENT['meetings']['report']['done']['message_send'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                })
      else:
        # done -> no sending
        return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
			'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title'], 
                	'message': settings.TEMPLATE_CONTENT['meetings']['report']['done']['message'],
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mrf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MeetingReportForm(initial={ 'num': Mt.num, 'title': Mt.title, 'when': visualiseDateTime(Mt.when), })
    title = settings.TEMPLATE_CONTENT['meetings']['report']['title'].format(unicode(Mt.num))
    return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['template'], {
                'title': title,
                'desc': settings.TEMPLATE_CONTENT['meetings']['report']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['report']['submit'],
                'form': form,
                })



