# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, IntegerField, FileField

from cms.functions import rmf

from members.models import Member
from locations.models import Location

def rename_report(i, f):
  fn = rmf('meetings', f, i.title)

  from os import sep
  return fn['name'] + fn['ext']

class Meeting(Model):
  num		= IntegerField(verbose_name='Numéro',primary_key=True)
  title		= CharField(verbose_name='Titre',max_length=100)
  when		= DateField(verbose_name='Date')
  time		= TimeField(verbose_name='Heure de début')
  location	= ForeignKey(Location,verbose_name='Lieu de Rencontre')
  deadline	= DateTimeField(verbose_name='Deadline')
  report        = FileField(verbose_name='Compte rendu', upload_to=rename_report,blank=True,null=True)
  
  def __unicode__(self):
    return unicode(self.title) + ' du ' + unicode(self.when)


def rename_attach(i, f):
  fn = rmf('meetings', f, str(i.meeting.num) + '-attachement')

  from os import sep
  return fn['name'] + fn['ext']

class Invitation(Model):
  meeting	= ForeignKey(Meeting)
  message	= CharField(max_length=5000,blank=True,null=True)
  attachement   = FileField(verbose_name='Annexe(s)', upload_to=rename_attach,blank=True,null=True)
  sent		= DateTimeField(blank=True,null=True)

  def __unicode__(self):
    if self.sent:
      return u'Invitations pour: ' + unicode(self.meeting) + u' envoyées à: ' + self.sent.strftime('%Y-%m-%d %H:%M')
    else:
      return u'Invitations pour: ' + unicode(self.meeting) + u' non encore envoyées.'


