import re
import email
import sys
import argparse
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, EmailMessage
from django.db.models import Q
from django.conf import settings

from members.models import Member

class Command(BaseCommand):
  def add_arguments(self, parser):

    # Positional arguments
    parser.add_argument('message', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    # Named (optional) arguments
    parser.add_argument(
      '--group', 
      dest='group',
      help='GROUP to send message to', 
      metavar='GROUP',
    )

  def handle(self, *args, **options):
    query = None
    message = ''
    subject = '[' + settings.EMAILS['tag'] + ' - ' + str.upper(str(options['group'])) + '] '
    emails = ()

    # get raw email message
    raw_message = email.message_from_string(options.get('message').read())
    sender = raw_message['from']
    group = options.get('group')
    subject += str(raw_message['subject'])

    self.stdout.write(self.style.NOTICE('''Groupmail from <'''+str(sender)+'''> to group: <'''+str(group)+'''>'''))

    # get members based on requested "group"
    if group == 'members':
      query = Member.objects.filter(Q(status=Member.ACT) | Q(status=Member.HON) | Q(status=Member.WBE))
    elif group == 'board':
      query = Member.objects.filter(role__isnull=False)
    else:
      query = None

    # get email parts from raw source
    if raw_message.is_multipart():
      for payload in raw_message.get_payload():
        message += payload.get_payload()
    else:
        message = raw_message.get_payload()

    # send(forward) mail to people of selected group
    if query is not None:
      for m in query:
        emails += (
	  (
          	subject,
          	message,
        	sender,
          	[m.email,],
	  ),
	)
        self.stdout.write(self.style.NOTICE('Prepared message for <'+str(m)+'>'))

    send_mass_mail(emails)
    self.stdout.write(self.style.SUCCESS('Emails sent!'))


