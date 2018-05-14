# coding=utf-8

from django.db.models import Model, CharField, URLField, EmailField, ForeignKey


class Contact(Model):
  first_name	= CharField(verbose_name='Prénom',max_length=100)
  last_name	= CharField(verbose_name='Nom',max_length=100)
  tel		= CharField(verbose_name='Téléphone',max_length=20,blank=True,null=True)
  mobile	= CharField(verbose_name='Mobile',max_length=20,blank=True,null=True)
  email		= EmailField(verbose_name='Courriel',blank=True,null=True)

  def __str__(self):
    return str(self.first_name) + ' ' + str.upper(self.last_name)

class Location(Model):
  name		= CharField(verbose_name='Nom',max_length=100)
  address	= CharField(verbose_name='Adresse',max_length=500)
  tel		= CharField(verbose_name='Téléphone',max_length=20,blank=True,null=True)
  email		= EmailField(verbose_name='Courriel',blank=True,null=True)
  website	= URLField(verbose_name='Site web',blank=True,null=True)
  contact	= ForeignKey(Contact,blank=True,null=True)

  def __str__(self):
    return str(self.name)

