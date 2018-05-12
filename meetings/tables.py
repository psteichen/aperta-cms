# coding=utf-8

from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils import timezone

from django_tables2.tables import Table
from django_tables2 import Column

from cms.functions import getSaison

from members.functions import gen_member_fullname
from attendance.models import Meeting_Attendance
from members.models import Member

from .models import Meeting, Invitation

#table for visualisation via django_tables2
class MeetingTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Présents/Excusés',empty_values=())
  details	= Column(verbose_name='Détails',empty_values=())

  def render_row_class(self, record):
    if record.when < timezone.now():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Meeting_Attendance.objects.filter(meeting=record,present=True).count(),Meeting_Attendance.objects.filter(meeting=record,present=False).count())

  def render_details(self, record):
    link = '<center><a class="btn btn-info btn-sm" href="/meetings/list/{}/"><i class="fa fa-list"></i></a></center>'.format(escape(record.num))
    return mark_safe(link)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'location', 'totals', 'details', )
    attrs = {"class": "table table-striped"}

class MgmtMeetingTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Présents/Excusés',empty_values=())
  details	= Column(verbose_name='Détails',empty_values=())
  send		= Column(verbose_name='Invitations',empty_values=())
  modify	= Column(verbose_name='Modifier',empty_values=())
  report	= Column(verbose_name='Compte rendu',empty_values=())

  def render_row_class(self, record):
    if record.when < timezone.now():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Meeting_Attendance.objects.filter(meeting=record,present=True).count(),Meeting_Attendance.objects.filter(meeting=record,present=False).count())

  def render_details(self, record):
    link = '<center><a class="btn btn-info btn-sm" href="/meetings/list/{}/"><i class="fa fa-list"></i></a></center>'.format(escape(record.num))
    return mark_safe(link)

  def render_send(self, record):
    sent = None
    try:
      I = Invitation.objects.get(meeting=record)
      sent = I.sent
    except: pass
    if sent: #already sent, resend?
      link = '<center><a class="btn btn-success btn-sm" href="/meetings/send/{}/" title="Renvoyer"><i class="fa fa-envelope"></i></a></center>'.format(escape(record.num))
    else: #not yet sent
      link = '<center><a class="btn btn-danger btn-sm" href="/meetings/send/{}/" title="Envoyer"><i class="fa fa-envelope"></i></a></center>'.format(escape(record.num))

    return mark_safe(link)

  def render_modify(self, record):
    link = '<center><a class="btn btn-danger btn-sm" href="/meetings/modify/{}/"><i class="fa fa-pencil"></i></a></center>'.format(escape(record.num))
    return mark_safe(link)

  def render_report(self, record):
    if record.report: #report exists, resubmit?
      link = '<center><a class="btn btn-success btn-sm" href="/meetings/report/{}/" title="Resoumettre"><i class="fa fa-file"></i></a></center>'.format(escape(record.num))
    else: #submit report
      link = '<center><a class="btn btn-danger btn-sm" href="/meetings/report/{}/" title="Soumettre"><i class="fa fa-file"></i></a></center>'.format(escape(record.num))
    return mark_safe(link)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'location', 'totals', 'details', 'send', 'modify', 'report', )
    attrs = {"class": "table table-striped"}


class MeetingMixin(Table):
  present	= Column(verbose_name=u'Présent',empty_values=())
  excused	= Column(verbose_name=u'Excusé',empty_values=())
  nonexcused	= Column(verbose_name=u'Non-excusé',empty_values=())

  class Meta:
    model = Meeting
    fields = ( 'present', 'excused', 'non-excused', )

class MeetingListingTable(MeetingMixin, Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  name		= Column(verbose_name=u'Nom (rôle)',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_name(self, record):
    roles = u''
    try:
      R = Role.objects.filter(member__id=record.id,year=getSaison())
      for r in R:
        roles += str(r.type.title)
        if r != R.last(): roles += u' ; '
    except Role.DoesNotExist:
      pass

    return record.last_name + ' ' + record.first_name + '( ' + roles + ')'

  def render_present(self, record):
    try:
      if Meeting_Attendance.objects.filter(meeting=record.meeting_num,member=record).only(present):
        return '<center>X</center>'
    except: pass

  def render_excused(self, record):
    try:
      if not Meeting_Attendance.objects.filter(meeting=record.meeting_num,member=record).only(present):
        return '<center>X</center>'
    except: pass

  def render_nonexcused(self, record):
    try:
      Meeting_Attendance.objects.filter(meeting=record.meeting_num,member=record).only(present)
    except:
      return '<center>X</center>'

  class Meta:
    model = Member
    fields = ( 'name', 'present', 'excused', 'non-excused', )
    attrs = {"class": "table table-striped"}

