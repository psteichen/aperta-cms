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
    #adjust settings from setup app
    try:
      S = Setup.objects.latest('cfg_date')
      if S.admin_email: 
        settings.SERVER_EMAIL = S.admin_email
        self.stdout.write(self.style.WARNING(u'SERVER_EMAIL = "'+S.admin_email+'"'))
      if S.org_name: 
        settings.TEMPLATE_CONTENT['meta']['logo']['title'] = S.org_name
        self.stdout.write(self.style.WARNING(u"TEMPLATE_CONTENT['meta']['logo']['title'] = \""+S.org_name+"\""))
        settings.TEMPLATE_CONTENT['meta']['title'] = S.org_name+" - Club Management System (CMS)"
        self.stdout.write(self.style.WARNING(u"TEMPLATE_CONTENT['meta']['title'] = \""+S.org_name+u" - Club Management System (CMS)\""))
        if S.default_email: 
          settings.DEFAULT_FROM_EMAIL = S.default_email
          self.stdout.write(self.style.WARNING(u"DEFAULT_FROM_EMAIL = \""+S.default_email+"\""))
      if S.default_footer: 
        settings.EMAILS['footer'] = S.default_footer
        self.stdout.write(self.style.WARNING(u"EMAILS['footer'] = \"\"\""+S.default_footer+"\"\"\""))
      if S.org_logo: 
        settings.TEMPLATE_CONTENT['meta']['logo']['img'] = S.org_logo
        self.stdout.write(self.style.WARNING(u"TEMPLATE_CONTENT['meta']['logo']['img'] = \""+S.org_logo+"\""))
    except Setup.DoesNotExist:
      self.stdout.write(self.style.ERROR(u"No setup data found in database. First you need to configure the system via the webinterface."))

    self.stdout.write(self.style.SUCCESS('Settings adjusted successfully.'))

