from django.contrib import admin

from .models import Meeting, Invitation, Invitee

from django import forms
class InvModelForm( forms.ModelForm ):
  message = forms.CharField( widget=forms.Textarea )
  class Meta:
     model = Invitation
     exclude = ( )

class InvAdmin( admin.ModelAdmin ):
    form = InvModelForm

admin.site.register(Meeting)
admin.site.register(Invitation, InvAdmin)
admin.site.register(Invitee)
