# coding=utf-8

from django_tables2.tables import Table

from .models import Location

#table for visualisation via django_tables2
class LocationTable(Table):

  class Meta:
    model = Location
    fields = ( 'name', 'address', 'tel', 'email', 'website', 'contact', )
    attrs = {"class": "table table-striped"}
