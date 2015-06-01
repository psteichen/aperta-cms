from django.contrib import admin

from .models import Meeting, Invitation, Invitee

admin.site.register(Meeting)
admin.site.register(Invitation)
admin.site.register(Invitee)
