# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, FileField, EmailField, ManyToManyField

from cms.functions import rmf

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
  location	= ForeignKey(Location,verbose_name='Lieu')
  deadline	= DateTimeField(verbose_name='Deadline')
  agenda        = CharField(verbose_name='Agenda',max_length=500)
  registration  = CharField(verbose_name='Code de régistration',max_length=25)
  
  def __str__(self):
    return str(self.title) + ' du ' + str(self.when)


def rename_attach(i, f):
  fn = rmf('events', f, str(i.event.pk) + '-attachement')

  from os import sep
  return fn['name'] + fn['ext']


class Invitation(Model):
  event		= ForeignKey(Event)
  message	= CharField(max_length=5000,blank=True,null=True)
  attachement   = FileField(verbose_name='Annexe(s)', upload_to=rename_attach,blank=True,null=True)
  sent		= DateTimeField(blank=True,null=True)

  def __str__(self):
    if self.sent:
      return u'Invitations pour: ' + str(self.event) + u' envoyées à: ' + self.sent.strftime('%Y-%m-%d %H:%M')
    else:
      return u'Invitations pour: ' + str(self.event) + u' non encore envoyées.'

class Partner(Model):
  name  = CharField(max_length=150)
  desc  = CharField(max_length=500)
  email = EmailField()

  def __str__(self):
    return str(self.name)

class Distribution(Model):
  event         = ForeignKey(Event)
  partners      = ManyToManyField(Partner)
  others        = CharField(max_length=500,blank=True,null=True)

  def __str__(self):
    return u'Distribution pour: ' + str(self.event)


class Participant(Model):
  event         = ForeignKey(Event)
  first_name    = CharField(max_length=150,verbose_name='Prénom')
  last_name     = CharField(max_length=150,verbose_name='Nom')
  email         = EmailField(verbose_name='E-mail')
  regcode       = CharField(max_length=25)
  affiliation   = ForeignKey(Partner,verbose_name='Affiliation',blank=True,null=True)

  class Meta:
    unique_together = ('event', 'first_name', 'last_name', 'email')

  def __str__(self):
    affil = ''
    if self.affiliation: affil = ' ['+str(self.affiliation)+']'
    return str(self.first_name) + ' ' + str(self.last_name) + ' <' + self.email + '>' + affil

