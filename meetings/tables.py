# coding=utf-8

from datetime import date

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from members.functions import gen_member_fullname
from attendance.models import Meeting_Attendance

from .models import Meeting

#table for visualisation via django_tables2
class MeetingTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Présents/Excusés',empty_values=())
  details	= Column(verbose_name='Détails',empty_values=())
  send		= Column(verbose_name='Invitations',empty_values=())
  modify	= Column(verbose_name='Modifier',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Meeting_Attendance.objects.filter(meeting=record,present=True).count(),Meeting_Attendance.objects.filter(meeting=record,present=False).count())

  def render_details(self, record):
    link = '<a class="btn btn-info btn-sm" href="/meetings/list/{}/"><span class="glyphicon glyphicon-list"></span></a>'.format(escape(record.num))
    return mark_safe(link)

  def render_send(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/meetings/send/{}/"><span class="glyphicon glyphicon-envelope"></span></a>'.format(escape(record.num))
    return mark_safe(link)

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/meetings/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a>'.format(escape(record.num))
    return mark_safe(link)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'location', 'totals', 'details', 'modify', )
    attrs = {"class": "table table-striped"}
