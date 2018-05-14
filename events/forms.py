# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, FileField, CheckboxSelectMultiple, RadioSelect

from .models import Event, Distribution, Participant

#event form
class EventForm(ModelForm):
  additional_message 	= CharField(label=u'Message supplémentaire',widget=Textarea(attrs={'placeholder': u"Message à transmettre dans l'invitation.",}),required=False)
  attachement 		= FileField(label=u'Annexe(s)',required=False)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'deadline', 'additional_message', 'attachement', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'location': Textarea(attrs={'placeholder': "Adresse détaillé du lieu de l'événement.",}),
      'agenda'  : Textarea(attrs={'placeholder': "Agenda ou description de l'événememt.",}),
      'deadline': TextInput(attrs={'type': 'date', 'id': 'dtpicker', }),
    }
    help_texts = {
      'location': '<a href="/locations/add/" >Ajouter un nouveau lieu de rencontre</a>',
    }

#distribution form
class DistributionForm(ModelForm):

  class Meta:
    model = Distribution
    fields = ( 'partners', 'others', )
    widgets = {
      'partners'        : CheckboxSelectMultiple(),
      'others'          : Textarea(attrs={'placeholder': '''Veuillez utiliser le format ci-dessous (une seule entrée par ligne) :
Prénom;Nom;Email'''}),
    }

#registration form
class RegistrationForm(ModelForm):

  class Meta:
    model = Participant
    fields = ( 'first_name', 'last_name', 'email', 'affiliation', )
    widgets = {
      'affiliation'     : RadioSelect(),
    }



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


