from django.contrib import admin

from .models import Product, Packaging, Price, Order, Receipt

admin.site.register(Product)
admin.site.register(Packaging)
admin.site.register(Price)
admin.site.register(Order)
admin.site.register(Receipt)
