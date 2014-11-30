from django.conf import settings
from django.db.models import Model, CharField, IntegerField, DecimalField, ForeignKey, DateField, ManyToManyField, ImageField 

from members.models import Member

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
  image		= ImageField(upload_to=settings.ORDER_IMAGE_DIR,blank=True,null=True)
  packaging	= ForeignKey(Packaging)
  price		= ForeignKey(Price)

class Order(Model):
  product	= ForeignKey(Product)
  amount	= IntegerField()

class Receipt(Model):
  member	= ForeignKey(Member)
  date		= DateField()
  order		= ManyToManyField(Order)
  total		= DecimalField(max_digits=6,decimal_places=2)

