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

  org_name		= CharField(initial=u'FIFTY-ONE Aperta',help_text=u"Nom officiel du club/de l'organisation")
  org_logo		= ImageField(initial='Logo Aperta',help_text=u"Logo officiel du club/de l'organisation")
  admin_email		= EmailField(initial='admin@aperta.lu',help_text=u"Adresse email de l'administrateur, qui recevera les messages d'erreurs et autres alertes système.")

  default_email 	= EmailField(initial=u'board@aperta.lu',help_text=u"Adresse email utilisée pour les automatiques aux utilisateurs et qui recevra aussi les réponses/questions des utilisateurs.")
  default_footer 	= CharField(widget=Textarea(),initial=u'''Amicalement,
Le comité APERTA
''',help_text=u"Le 'footer' des envoi emails automatique")

  optional_apps		= MultipleChoiceField(widget=CheckboxSelectMultiple(),choices=APPS,help_text=u"Application(s) optionnelle(s), ne faisant pas partie du coeur du système.",required=False)

