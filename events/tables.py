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

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Event_Attendance.objects.filter(event=record,present=True).count(),Event_Attendance.objects.filter(event=record,present=False).count())

  def render_details(self, record):
    link = '<a class="btn btn-info btn-sm" href="/events/list/{}/"><i class="fa fa-list"></i></a>'.format(escape(record.pk))
    return mark_safe(link)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'location', 'totals', 'details', )
    attrs = {"class": "table table-striped"}


class MgmtEventTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Présents/Excusés',empty_values=())
  details	= Column(verbose_name='Détails',empty_values=())
  send		= Column(verbose_name='Invitations',empty_values=())
  modify	= Column(verbose_name='Modifier',empty_values=())
#  photos	= Column(verbose_name='Photos',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Event_Attendance.objects.filter(event=record,present=True).count(),Event_Attendance.objects.filter(event=record,present=False).count())

  def render_details(self, record):
    link = '<center><a class="btn btn-info btn-sm" href="/events/list/{}/"><i class="fa fa-list"></i></a></center>'.format(escape(record.pk))
    return mark_safe(link)

  def render_send(self, record):
    sent = None
    try:
      I = Invitation.objects.get(event=record)
      sent = I.sent
    except: pass
    if sent: #already sent, resend?
      link = '<center><a class="btn btn-success btn-sm" href="/events/send/{}/" title="Renvoyer"><i class="fa fa-envelope"></i></a></center>'.format(escape(record.pk))
    else: #not yet sent
      link = '<center><a class="btn btn-danger btn-sm" href="/events/send/{}/" title="Envoyer"><i class="fa fa-envelope"></i></a></center>'.format(escape(record.pk))

    return mark_safe(link)

  def render_modify(self, record):
    link = '<center><a class="btn btn-danger btn-sm" href="/events/modify/{}/"><i class="fa fa-pencil"></i></a></center>'.format(escape(record.pk))
    return mark_safe(link)

#  def render_photos(self, record):
#    if record.photos:
#      link = '<center><a class="btn btn-success btn-sm" href="/events/photos/{}/" title="Resoumettre"><i class="fa fa-file"></i></a></center>'.format(escape(record.pk))
#    else: #submit report
#      link = '<center><a class="btn btn-danger btn-sm" href="/events/photos/{}/" title="Soumettre"><i class="fa fa-file"></i></a></center>'.format(escape(record.pk))
#    return mark_safe(link)

  class Meta:
    model = Event
#    fields = ( 'title', 'when', 'location', 'totals', 'details', 'send', 'modify', 'photos', )
    fields = ( 'title', 'when', 'location', 'totals', 'details', 'send', 'modify', )
    attrs = {"class": "table table-striped"}


