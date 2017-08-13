#coding=utf-8

from django_tables2.tables import Table
from django_tables2 import Column

from .models import BankExtract, BalanceSheet

#table for visualisation via django_tables2
class BankExtractTable(Table):
  ynum		= Column(verbose_name=u'Détails', empty_values=())

  def render_ynum(self, value, record):
    return unicode(record)

  class Meta:
    model = BankExtract
    fields = ( 'ynum', 'scan', )
    attrs = {"class": "table table-striped"}

class BalanceSheetTable(Table):

  class Meta:
    model = BalanceSheet
    fields = ( 'year', 'scan', )
    attrs = {"class": "table table-striped"}
