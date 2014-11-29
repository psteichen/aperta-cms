# coding=utf-8

from datetime import date

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from .models import Product

#table for visualisation via django_tables2
class ProductTable(Table):
  details	= Column(verbose_name='Détails',empty_values=())
  modify	= Column(verbose_name='Modifier',empty_values=())

  def render_details(self, record):
    link = '<a class="btn btn-default btn-sm" href="/selling/list/{}/"><span class="glyphicon glyphicon-list"></span></a>'.format(escape(record.pk))
    return mark_safe(link)

  def render_modify(self, record):
    link = '<a class="btn btn-default btn-sm" href="/selling/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a>'.format(escape(record.pk))
    return mark_safe(link)

  class Meta:
    model = Product
    fields = ( 'title', 'desc', 'packaging.desc', 'packaging.content', 'packaging.units', 'price.buying', 'price.selling', )
    attrs = {"class": "table table-striped"}
