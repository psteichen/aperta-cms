# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, FileField, OneToOneField

from members.models import Member
from locations.models import Location

class Event(Model):
  MEET = 0
  OTH = 1
  TYPES = (
    (MEET, 'Réunion statutaire'),
    (OTH,  'Autre Evénement/Rencontre'),
  )

  title		= CharField(verbose_name='Titre',max_length=100)
  when		= DateField(verbose_name='Date')
  time		= TimeField(verbose_name='Heure de début')
  location	= ForeignKey(Location,verbose_name='Lieu de Rencontre',blank=True,null=True)
  deadline	= DateField(verbose_name='Deadline')
  attachement	= FileField(verbose_name='Notice détaillée',upload_to='events',blank=True,null=True)
  
  def __unicode__(self):
    return unicode(self.title) + ' du ' + unicode(self.when)


class Invitation(Model):
  event		= OneToOneField(Event)
  message	= CharField(max_length=5000)
  sent		= DateTimeField(blank=True,null=True)

  def __unicode__(self):
    sent = ''
    if self.sent:
      sent = u' envoyé le ' + unicode(self.sent)
    return unicode(self.event) + sent
