# coding=utf-8

from datetime import date

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from members.functions import gen_member_fullname
from attendance.models import Event_Attendance

from .models import Event

#table for visualisation via django_tables2
class EventTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Présents/Excusés',empty_values=())
  details	= Column(verbose_name='Détails',empty_values=())
  modify	= Column(verbose_name='Modifier',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Event_Attendance.objects.filter(event=record,present=True).count(),Event_Attendance.objects.filter(event=record,present=False).count())

  def render_details(self, record):
    link = '<a class="btn btn-default btn-sm" href="/events/list/{}/"><span class="glyphicon glyphicon-list"></span></a>'.format(escape(record.pk))
    return mark_safe(link)

  def render_modify(self, record):
    link = '<a class="btn btn-default btn-sm" href="/events/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a>'.format(escape(record.pk))
    return mark_safe(link)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'location', 'totals', 'details', 'modify', )
    attrs = {"class": "table table-striped"}
