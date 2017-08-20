#coding=utf-8

from django.forms import ModelForm
from django.forms import Textarea, CheckboxSelectMultiple

from .models import Setup

#setup form
class SetupForm(ModelForm):

  class Meta:
    model = Setup
    fields = ( 'org_name', 'org_logo', 'admin_email', 'default_email', 'default_footer', 'optional_apps', )
    labels = {
      'org_name'	: u"Nom officiel du club/de l'organisation",
      'org_logo'	: u"Logo officiel du club/de l'organisation",
      'admin_email'	: u"Adresse email de l'administrateur",
      'default_email'	: u"Adresse email 'par défaut'",
      'default_footer'	: u"Salutation 'par défaut'",
      'optional_apps'	: u"Applications(s) optionnelle(s)",
    }
    widgets = {
      'default_footer'	: Textarea(),
      'optional_apps'	: CheckboxSelectMultiple(),
    }
    help_texts = {
      'org_name'	: u"C'est le nom qui sera affichée dans l'entête du site.",
      'org_logo'	: u"Ce logo sera affiché dans l'entête du site.",
      'admin_email'	: u"L'administrateur recevera les messages d'erreurs et autres alertes système.",
      'default_email'	: u"Adresse email utilisée pour les automatiques aux utilisateurs et qui recevra aussi les réponses/questions des utilisateurs.",
      'default_footer'	: u"Le 'footer' des envoi emails automatique",
      'optional_apps'	: u"Ne faisant pas partie du coeur du système.",
    }

