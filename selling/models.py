from django.db.models import Model, CharField, IntegerField, DecimalField, ForeignKey, DateField 

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
  packaging	= ForeignKey(Packaging)
  price		= ForeignKey(Price)

class Order(Model):
  date		= DateField()
  product	= ForeignKey(Product)
  amount	= IntegerField()
  selling	= DecimalField(max_digits=6,decimal_places=2)

