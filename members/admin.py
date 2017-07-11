from django.contrib import admin

from .models import Member, Role, RoleType

admin.site.register(Member)
admin.site.register(Role)
admin.site.register(RoleType)
