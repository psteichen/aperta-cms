# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, FileField

from .models import Event

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
      'deadline': TextInput(attrs={'type': 'date', 'id': 'dtpicker', }),
    }
    help_texts = {
      'location': '<a href="/locations/add/" >Ajouter un nouveau lieu de rencontre</a>',
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


