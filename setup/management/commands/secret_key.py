#coding=utf-8

from django.utils.crypto import get_random_string

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  help = 'Adjusts settings file based on inital config via web interface'

  def handle(self, *args, **options):
    # create secret key
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    generated_key = get_random_string(50, chars)
    self.stdout.write(self.style.SUCCESS(u'settings.SECRET_KEY = "'+generated_key+'"'))
    options['secret_key'] = generated_key

