#coding=utf-8

from django.db.models import Model, EmailField, CharField, ImageField, DateTimeField
from django.core.validators import validate_comma_separated_integer_list

from cms.functions import rmf

def rename_logo(i, f):
  name = unicode(i.nom)
  fn = rmf('', f, name)

  from os import sep
  return fn['name'] + fn['ext']


class Setup(Model):
  meetings 	= 0
  members 	= 1
  events 	= 2
  locations 	= 3
  finance 	= 4
  APPS = (
#default    ( meetings	, u'Réunions Statutaires'),
#default    ( members	, u'Membres'), 
#default    ( events	, u'Évènements'), 
#default    ( locations	, u'Lieux de Rencontres'), 
    ( finance	, u'Trésorerie (pour gérer les comptes annuels et les extraits bancaires)'), 
  )

  cfg_date		= DateTimeField()
  org_name		= CharField(max_length=100)
  org_logo		= ImageField(upload_to=rename_logo,blank=True,null=True)
  admin_email		= EmailField()
  default_email 	= EmailField()
  default_footer 	= CharField(max_length=500,blank=True,null=True)
  optional_apps		= CharField(max_length=50,choices=APPS,validators=[validate_comma_separated_integer_list],blank=True,null=True)


  def __unicode__(self):
    return self.org_name

