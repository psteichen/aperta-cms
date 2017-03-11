#coding=utf-8

from datetime import date

from django.forms import Form, ModelForm, TextInput, Textarea, ModelChoiceField, BooleanField, CharField
from django.conf import settings

from .models import Member, Role

#role form
class RoleForm(ModelForm):

  class Meta:
    model = Role
    fields = ( 'title', 'desc', 'start_date', 'end_date', ) 
    widgets = {
      'start_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker',}),
      'end_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker2',}),
    }


#meeting form
class MemberForm(ModelForm):

  class Meta:
    model = Member
    fields = ( 'photo', 'first_name', 'last_name', 'email', 'start_date', 'status', ) 
    widgets = {
      'email'		: TextInput(attrs={'type': 'email', }),
      'start_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker',}),
    }


#modify forms
class ListMembersForm(Form):
  members = ModelChoiceField(label='Member',queryset=Member.objects.all().order_by('last_name'))

class ModifyMemberForm(MemberForm):
  role = CharField(label=u'Rôle:',widget=TextInput(attrs={'disabled': 'disabled', }),required=False)
  mod_role = BooleanField(label=u'Modifier le rôle:',required=False)
  add_role = BooleanField(label=u'Ajouter un rôle:',required=False)

class ModifyRoleForm(RoleForm):
  class Meta:
    model = Role
    fields = ( 'title', 'desc', 'start_date', 'end_date', ) 
    widgets = {
      'start_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker',}),
      'end_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker2',}),
    }


