#coding=utf-8

from datetime import date

from django_tables2.tables import Table
from django_tables2 import Column

from django.utils.safestring import mark_safe
from django.utils.html import escape

from attendance.models import Meeting_Attendance

from .models import Member, Role

#table for visualisation via django_tables2
class MemberTable(Table):
  role		= Column(verbose_name=u'Rôle',empty_values=())
  meetings	= Column(verbose_name=u'Réunions statutaires<br/>(présent / excusé)',empty_values=())

  def render_last_name(self, value):
    return unicode.upper(value)

  def render_role(self, value, record):
    try:
      role = Role.objects.get(member__id=record.id)
      if role.end_date:
        return unicode(role.title) + ' (' + unicode(role.start_date) + ' - ' + unicode(role.end_date) +')'
      else:
        return unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
    except:
      return ''

  def render_meetings(self, record):
    MA = Meeting_Attendance.objects.filter(member=record)
    return '{} / {}'.format(MA.filter(present=True).count(),MA.filter(present=False).count())

  class Meta:
    model = Member
    fields = ( 'first_name', 'last_name', 'email', 'start_date', 'end_date', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-striped"}

#management table
class MgmtMemberTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  role		= Column(verbose_name=u'Rôle',empty_values=())
  meetings	= Column(verbose_name=u'Réunions statutaires<br/>(présent / excusé)',empty_values=())
  modify	= Column(verbose_name=u'Modifier',empty_values=())

  def render_row_class(self, value, record):
    cl = ''
    if record.status == Member.ACT:
      cl = 'success'
    if record.status == Member.WBE:
      cl = 'info'

    att = record.attendance.all().count()
    exc = record.excused.all().count()
    if att == 0:
      cl = 'warning'
    if record.end_date or record.status == Member.STB or (att == 0 and exc == 0):
      cl = 'danger'

    return cl

  def render_last_name(self, value):
    return unicode.upper(value)

#  def render_start_date(self, value):
#    return format_datetime(value)

#  def render_end_date(self, value):
#    return format_datetime(value)

  def render_role(self, value, record):
    try:
      role = Role.objects.get(member__id=record.id)
      if role.end_date:
        return unicode(role.title) + ' (' + unicode(role.start_date) + ' - ' + unicode(role.end_date) +')'
      else:
        return unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
    except:
      return ''

  def render_meetings(self, record):
    MA = Meeting_Attendance.objects.filter(member=record)
    return '{} / {}'.format(MA.filter(present=True).count(),MA.filter(present=False).count())

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/members/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a>'.format(escape(record.pk))
    return mark_safe(link)


  class Meta:
    model = Member
    fields = ( 'first_name', 'last_name', 'email', 'start_date', 'end_date', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-striped"}
