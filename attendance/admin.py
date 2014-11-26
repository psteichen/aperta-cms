from django.contrib import admin

from .models import Meeting_Attendance, Event_Attendance

admin.site.register(Meeting_Attendance)
admin.site.register(Event_Attendance)
