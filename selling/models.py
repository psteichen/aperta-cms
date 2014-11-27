from django.db.models import Model, CharField, IntegerField, DecimalField, ForeignKey

class Packaging(Model):
  desc		= CharField(max_length=500)
  content	= IntegerField()
  units		= CharField(max_length=50)

class Price(Model):
  buying	= DecimalField(max_digits=5,decimal_places=2)
  selling	= DecimalField(max_digits=5,decimal_places=2)

class Product(Model):
  title		= CharField(max_length=250)
  desc		= CharField(max_length=500)
  packaging	= ForeignKey(Package)
  price		= ForeignKey(Price)

