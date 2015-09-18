#coding=utf-8

from datetime import date

from django_tables2.tables import Table
from django_tables2 import Column

from django.utils.safestring import mark_safe
from django.utils.html import escape

from .models import Category, Page

#web table
class CategoriesTable(Table):
  pages		= Column(verbose_name=u'Pages',empty_values=())
  add		= Column(verbose_name=u'Ajouter une page',empty_values=())
  modify	= Column(verbose_name=u'Modifier la catégorie',empty_values=())

  def render_pages(self, record):
    links = []
    for p in record.pages.all():
      links.append('<a href="/web/page/modify/{}/">{}</a>'.format(escape(p.pk),escape(p.title)))
    return mark_safe(' ; '.join(l in links))

  def render_add(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/web/page/add/{}/"><span class="glyphicon glyphicon-plus"></span></a>'.format(escape(record.pk))
    return mark_safe(link)

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/web/category/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a>'.format(escape(record.pk))
    return mark_safe(link)

  class Meta:
    model = Category
    fields = ( 'title', 'index', 'pages', )
    attrs = {"class": "table table-striped"}

