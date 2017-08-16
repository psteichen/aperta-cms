#coding=utf-8

from django.forms import Form, CharField, ImageField, EmailField, MultipleChoiceField
from django.forms import Textarea, CheckboxSelectMultiple


#setup form
class SetupForm(Form):
  APPS = (
#default    ( 'meetings'	, u'Réunions Statutaires'),
#default    ( 'members'		, u'Membres'), 
#default    ( 'events'		, u'Évènements'), 
#default    ( 'locations'	, u'Lieux de Rencontres'), 
    ( 'finance'		, u'Trésorerie (pour gérer les comptes annuels et les extraits bancaires)'), 
  )

  org_name		= CharField(help_text='Official name of the Club/Organisation')
  org_logo		= ImageField(help_text='Official logo of the Club/Organisation')
  admin_email		= EmailField(initial='admin@aperta.lu',help_text='Email oddress f the Site Admin, which will get error messages and system messages.')

  default_sender 	= CharField(widget=Textarea(),initial='FIFTY-ONE Aperta',help_text='Header of the "sending email".')
  default_email 	= EmailField(initial='board@aperta.lu',help_text='Email address where all messages are being send from and whoch will get "user" replies.')
  default_footer 	= CharField(widget=Textarea(),initial='''Amicalement,
Le comité APERTA
''')

  opional_apps		= MultipleChoiceField(widget=CheckboxSelectMultiple(),choices=APPS,help_text='Optional applications not part of the core system.')

