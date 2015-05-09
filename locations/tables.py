# coding=utf-8

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from .models import Location

#table for visualisation via django_tables2
class LocationTable(Table):

  class Meta:
    model = Location
    fields = ( 'name', 'address', 'tel', 'email', 'website', 'contact', )
    attrs = {"class": "table table-striped"}

class MgmtLocationTable(Table):
  modify	= Column(verbose_name='Modifier',empty_values=())

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/locations/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a>'.format(escape(record.pk))
    return mark_safe(link)


  class Meta:
    model = Location
    fields = ( 'name', 'address', 'tel', 'email', 'website', 'contact', 'modify', )
    attrs = {"class": "table table-striped"}
