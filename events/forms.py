# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, FileField, CheckboxSelectMultiple, RadioSelect

from .models import Event, Partner, Distribution, Participant

#event form
class EventForm(ModelForm):
  additional_message 	= CharField(label=u'Message supplémentaire',widget=Textarea(attrs={'placeholder': u"Message à transmettre dans l'invitation.",}),required=False)
  attachement 		= FileField(label=u'Annexe(s)',required=False)
  partners 		= ModelChoiceField(label=u'Club(s) partenaire(s)',queryset=Partner.objects.all(),widget=CheckboxSelectMultiple(),required=False)
  others 		= CharField(label=u"Listes d'invités",required=False,widget=Textarea(attrs={'placeholder': 'Prénom;Nom;Email'}),help_text='Veuillez utiliser le format ci-dessus (une seule entrée par ligne)')

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'agenda', 'deadline', 'additional_message', 'attachement', 'partners', 'others', )
    widgets = {
      'when'		: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'		: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'location'	: Textarea(attrs={'placeholder': "Adresse détaillé du lieu de l'événement.",}),
      'agenda'  	: Textarea(attrs={'placeholder': "Agenda ou description de l'événememt.",}),
      'deadline'	: TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }
    help_texts = {
      'deadline'	: 'Date de clôture des inscriptions',
    }

#registration form
class RegistrationForm(ModelForm):

  class Meta:
    model = Participant
    fields = ( 'first_name', 'last_name', 'email', )
#    fields = ( 'first_name', 'last_name', 'email', 'affiliation', )
#    widgets = {
#      'affiliation'     : RadioSelect(),
#    }



#modify wizard forms
class ListEventsForm(Form):
  events = ModelChoiceField(queryset=Event.objects.all())

class ModifyEventForm(ModelForm):
  attendance = BooleanField(label='Inscrire/excuser un membre')

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'deadline', 'attendance',  )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'date', 'id': 'dtpicker', }),
    }
    help_texts = {
      'location': '<a href="/locations/add/" >Ajouter un nouveau lieu de rencontre</a>',
    }


