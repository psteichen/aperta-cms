# coding=utf-8

from datetime import date

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField

from members.models import Member

from .models import Meeting

#add meeting form
class AddMeetingForm(ModelForm):
  new_location		= BooleanField(label='Créer un nouveau lieu de rencontre',required=False)
  additional_message 	= CharField(label='Message supplémentaire',widget=Textarea(attrs={'placeholder': "Message à transmettre dans l'invitation.",}),required=False)
  send 			= BooleanField(label='Envoi direct des invitations',required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'new_location',  'deadline', 'additional_message', 'attachement', 'send', )
    widgets = {
#      'title'	: TextInput(attrs={'readonly': 'readonly', }),
      'when'	: TextInput(attrs={'type': 'date', }),
#      'time'	: TextInput(attrs={'type': 'time', }),
      'deadline': TextInput(attrs={'type': 'date', }),
      'num'	: HiddenInput(),
    }


#wouldbe form
class WouldBeForm(ModelForm):

  class Meta:
    model = Member
    fields = ( 'first_name', 'last_name', 'email', ) 
    widgets = {
      'email'		: TextInput(attrs={'type': 'email', }),
    }

#modify wizard forms
class ListMeetingsForm(Form):
  meetings = ModelChoiceField(queryset=Meeting.objects.all().order_by('-num'))

class ModifyMeetingForm(ModelForm):
  attendance = BooleanField(label='Inscrire/excuser un membre')

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'attendance', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
    }
