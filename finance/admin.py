from django.contrib import admin

from .models import BankExtract, BalanceSheet

admin.site.register(BankExtract)
admin.site.register(BalanceSheet)
