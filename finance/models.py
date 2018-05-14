#coding=utf-8

from django.db.models import Model, DateTimeField, IntegerField, DecimalField, ForeignKey, CharField, FileField, DateField

from cms.functions import rmf

from members.models import Member

class Invoice(Model):
  MEMBERSHIP 	= 0
  ACOMPTE 	= 1
  ACTION 	= 2
  DONATION 	= 3
  TYPES = (
    (MEMBERSHIP,u'Cotisation'),
    (ACOMPTE,u'Avance'),
    (ACTION,u'Activité'),
    (DONATION,u'Don'),
  )
  date		= DateTimeField()
  type		= IntegerField(choices=TYPES)
  amount	= DecimalField(max_digits=10,decimal_places=2)
  recipient	= ForeignKey(Member)
  
  def __str__(self):
    return ''


class Payment(Model):
  date		= DateTimeField()
  invoice	= ForeignKey(Invoice)
  sender	= ForeignKey(Member)

  def __str__(self):
    return ''

def rename_be_scan(i, f):
  fn = rmf('bank', f, str(i))

  from os import sep
  return fn['name'] + fn['ext']

class BankExtract(Model):
  year		= CharField(verbose_name='Année',max_length=4)
  num		= IntegerField()
  date		= DateField(verbose_name='état du')
  scan  	= FileField(upload_to=rename_be_scan)

  def __str__(self):
    return self.year+'-'+str(self.num) + u' (état du ' + str(self.date) +')'

def rename_bs_scan(i, f):
  fn = rmf('balance', f, str(i))

  from os import sep
  return fn['name'] + fn['ext']

class BalanceSheet(Model):
  year		= CharField(verbose_name='Année',max_length=15)
  date        	= DateField(verbose_name='état du')
  scan        	= FileField(verbose_name='Document',upload_to=rename_bs_scan)

  def __str__(self):
    return self.year+ u' (état du ' + str(self.date) +')'

