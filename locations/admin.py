from django.contrib import admin

from .models import Location, Contact

admin.site.register(Contact)
admin.site.register(Location)
