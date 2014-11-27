from datetime import date

from django.forms import Form, ModelForm, TextInput, Textarea, ModelChoiceField, BooleanField
from django.conf import settings

from .models import Member, Role

#role form
class RoleForm(ModelForm):

  class Meta:
    model = Role
    fields = ( 'title', 'desc', 'start_date', 'end_date', 'member', ) 
    widgets = {
      'start_date'	: TextInput(attrs={'type': 'date', }),
      'end_date'	: TextInput(attrs={'type': 'date', }),
    }


#meeting form
class MemberForm(ModelForm):

  class Meta:
    model = Member
    fields = ( 'first_name', 'last_name', 'email', 'start_date', 'status', ) 
    widgets = {
      'email'		: TextInput(attrs={'type': 'email', }),
      'start_date'	: TextInput(attrs={'type': 'date', }),
    }


#modify forms
class ListMembersForm(Form):
  members = ModelChoiceField(label='Member',queryset=Member.objects.all().order_by('last_name'))

class ModifyMemberForm(MemberForm):
  role = BooleanField(label='Modify role:',required=False)

class ModifyRoleForm(RoleForm):
  class Meta:
    model = Role
    fields = ( 'title', 'desc', 'start_date', 'end_date', ) 
    widgets = {
      'start_date'	: TextInput(attrs={'type': 'date', }),
      'end_date'	: TextInput(attrs={'type': 'date', }),
    }

