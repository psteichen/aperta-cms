#coding=utf-8

from django.forms import Form, CharField, ImageField, EmailField, MultipleChoiceField
from django.forms import Textarea, CheckboxSelectMultiple


#setup form
class SetupForm(Form):
  APPS = (
    ( 'meetings'	, u'Réunions Statutaires'),
    ( 'members'		, u'Membres'), 
    ( 'finance'		, u'Trésorerie'), 
    ( 'events'		, u'Évènements'), 
    ( 'locations'	, u'Lieux de Rencontres'), 
  )

  name			= CharField()
  logo			= ImageField()
  admin_email		= EmailField()

  default_sender 	= CharField(widget=Textarea(),initial='FIFTY-ONE Aperta')
  default_email 	= EmailField()
  default_footer 	= CharField(widget=Textarea(),initial='''Amicalement,
Le comité APERTA
''')

  apps			= MultipleChoiceField(widget=CheckboxSelectMultiple(),choices=APPS)

