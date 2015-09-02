#coding=utf-8

from django.db.models import Model, DateTimeField, IntegerField, DecimalField, ForeignKey, CharField, FileField

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
  
  def __unicode__(self):
    return ''


class Payment(Model):
  date		= DateTimeField()
  invoice	= ForeignKey(Invoice)
  sender	= ForeignKey(Member)

  def __unicode__(self):
    return ''


def rename_scan(i, f):
  fn = rmf('bank', f, unicode(i))

  from os import sep
  return fn['name'] + fn['ext']

class BankExtract(Model):
  year		= CharField(max_length=4)
  num		= IntegerField()
  scan  	= FileField(upload_to=rename_scan)

  def __unicode__(self):
    return self.year+'-'+str(self.num)

