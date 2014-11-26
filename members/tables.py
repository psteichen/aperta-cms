#coding=utf-8

from datetime import date

from django_tables2.tables import Table
from django_tables2 import Column

from attendance.models import Meeting_Attendance

from .models import Member, Role

#table for visualisation via django_tables2
class MemberTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  role		= Column(empty_values=())
  meetings	= Column(verbose_name='Réunions statutaires (présent / excusé)',empty_values=())

  def render_row_class(self, value, record):
    att = record.attendance.all().count()
    exc = record.excused.all().count()

    if record.end_date or record.status == Member.STB or (att == 0 and exc == 0):
      return 'danger'
    elif att == 0:
      return 'warning'
    elif record.status == Member.ACT:
      return 'success'
    elif record.status == Member.WBE:
      return 'info'

  def render_last_name(self, value):
    return unicode.upper(value)

#  def render_start_date(self, value):
#    return format_datetime(value)

#  def render_end_date(self, value):
#    return format_datetime(value)

  def render_role(self, value, record):
    try:
      role = Role.objects.get(member__id=record.id)
      return unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
    except:
      pass

  def render_meetings(self, record):
    return '{} / {}'.format(Meeting_Attendance.objects.filter(member=record,present=True).count(),Meeting_Attendance.objects.filter(member=record,present=False).count())

  class Meta:
    model = Member
    fields = ( 'first_name', 'last_name', 'email', 'start_date', 'end_date', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-hover"}

