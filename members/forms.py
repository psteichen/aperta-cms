#coding=utf-8

from datetime import date

from django.forms import Form, ModelForm, TextInput, Textarea, ModelChoiceField, BooleanField, CharField
from django.conf import settings

from .models import Member, Role, RoleType


# members #
###########
class MemberForm(ModelForm):

  class Meta:
    model = Member
    fields = ( 'photo', 'first_name', 'last_name', 'address', 'prefix', 'phone', 'mobile', 'email', 'start_date', 'status', ) 
    widgets = {
      'address'		: Textarea(attrs={'cols': 20, 'rows': 5, }),
      'phone'		: TextInput(attrs={'type': 'tel', }),
      'email'		: TextInput(attrs={'type': 'email', }),
      'start_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker',}),
    }


# roles #
#########
class RoleForm(ModelForm):

  class Meta:
    model = Role
    fields = ( 'type', 'year', 'member', ) 

class RoleTypeForm(ModelForm):

  class Meta:
    model = RoleType
    fields = ( 'title', 'desc', 'type', ) 


