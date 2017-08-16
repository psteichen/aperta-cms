from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin

#from .models import User, Member, Role, RoleType
from .models import  Member, Role, RoleType

#admin.site.register(User, UserAdmin)
admin.site.register(Member)
admin.site.register(Role)
admin.site.register(RoleType)
