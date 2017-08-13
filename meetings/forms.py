# coding=utf-8

from datetime import date

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, ModelMultipleChoiceField, CheckboxSelectMultiple, FileField, IntegerField
from django.forms.models import modelformset_factory, BaseModelFormSet

from members.functions import get_active_members

from .models import Meeting, Invitee

#meeting forms
class MeetingForm(ModelForm):
  additional_message 	= CharField(label='Message supplémentaire',widget=Textarea(attrs={'placeholder': "Message à transmettre dans l'invitation.",}),required=False)
  attachement 		= FileField(label='Annexe(s)',required=False)
#  send 			= BooleanField(label='Envoi direct des invitations',required=False)

  class Meta:
    model = Meeting
#    fields = ( 'title', 'when', 'time', 'location', 'num', 'deadline', 'additional_message', 'attachement', 'send', )
    fields = ( 'title', 'when', 'time', 'location', 'num', 'deadline', 'additional_message', 'attachement', )
    widgets = {
#      'title'	: TextInput(attrs={'readonly': 'readonly', }),
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
      'num'	: HiddenInput(),
    }


#invite formset
class InviteeForm(ModelForm):

  class Meta:
    model = Invitee
    fields = ( 'first_name', 'last_name', 'email', 'type', )

#this is needed to set the queryset to none by default
class BaseInviteeFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseInviteeFormSet, self).__init__(*args, **kwargs)
        self.queryset = Invitee.objects.none()

InviteeFormSet = modelformset_factory(Invitee, form=InviteeForm, formset=BaseInviteeFormSet, extra=3)


#modify forms
class ModifyMeetingForm(ModelForm):

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'deadline', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }
    help_texts = {
      'location': '<a href="/locations/add/" >Ajouter un nouveau lieu de rencontre</a>',
    }


#report forms
class MeetingReportForm(Form):
  num		= IntegerField(widget=HiddenInput())
  title		= CharField(label=u'Titre',widget=TextInput(attrs={'readonly': 'readonly', }))
  when		= CharField(label=u'Date',widget=TextInput(attrs={'readonly': 'readonly', }))
  report	= FileField(label='Compte rendu')
  send 		= BooleanField(label='Envoi du compte rendu aux membres',required=False)

