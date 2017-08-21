#coding=utf-8

from random import SystemRandom
from string import ascii_letters, digits, punctuation

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.sites.models import Site

from setup.models import Setup

class Command(BaseCommand):
  help = 'Adjusts settings file based on inital config via web interface'

  def handle(self, *args, **options):
    # create secret key
    generated_key = u''.join([SystemRandom().choice(ascii_letters + digits + punctuation) for _ in range(50)])
#    settings.SECRET_KEY	= generated_key
    self.stdout.write(self.style.SUCCESS(u"settings.SECRETY_KEY = "+generated_key))

    #adjust settings from setup app
    try:
      S = Setup.objects.latest('cfg_date')
      if S.admin_email: 
#        settings.SERVER_EMAIL = S.admin_email
        self.stdout.write(self.style.SUCCESS(u"settings.SERVER_EMAIL = "+S.admin_email))
      if S.name: 
#        settings.TEMPLATE_CONTENT['meta']['logo']['title'] = S.name
        self.stdout.write(self.style.SUCCESS(u"settings.TEMPLATE_CONTENT['meta']['logo']['title'] = "+S.name))
#        settings.TEMPLATE_CONTENT['meta']['title'] = S.name+" - Club Management System (CMS)"
        self.stdout.write(self.style.SUCCESS(u"settings.TEMPLATE_CONTENT['meta']['title'] = "+S.name+u" - Club Management System (CMS)"))
        if S.default_email: settings.DEFAULT_FROM_EMAIL = "'"+S.name+"' <"+S.default_email+">"
      if S.default_footer: 
#        settings.EMAILS['footer'] = S.default_footer
        self.stdout.write(self.style.SUCCESS(u"settings.EMAILS['footer'] = "+S.default_footer))
      if S.logo: 
#        settings.TEMPLATE_CONTENT['meta']['logo']['img'] = S.logo
        self.stdout.write(self.style.SUCCESS(u"settings.TEMPLATE_CONTENT['meta']['logo']['img'] = "+S.logo))
    except Setup.DoesNotExist:
      self.stdout.write(self.style.ERROR(u"No setup data found in database. First you need to configure the system via the webinterface."))

    # finally set allowd host
    site = Site.objects.get(pk=settings.SITE_ID)
#    settings.ALLOWED_HOSTS[0] = site.name
    self.stdout.write(self.style.SUCCESS(u"settings.ALLOWED_HOSTS[0] = "+site.name))

# file method:
#      with FileInput(fileToSearch, inplace=True, backup='.bak') as file:
#      for line in file:
#        line.replace(textToSearch, textToReplace)

    self.stdout.write(self.style.SUCCESS('Settings adjusted successfully.'))

