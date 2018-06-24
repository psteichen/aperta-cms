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
    subject = settings.EMAILS['tag'] + ' [' + str.upper(str(options['group'])) + '] '
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
    body = ''
    if raw_message.preamble is not None:
      body += raw_message.preamble

    for part in raw_message.walk():
      if part.is_multipart():
        continue

      ctype = part.get_content_type()
      cte = part.get_params(header='Content-Transfer-Encoding')
      if (ctype is not None and not ctype.startswith('text')) or \
       (cte is not None and cte[0][0].lower() == '8bit'):
        part_body = part.get_payload(decode=False)
      else:
        charset = part.get_content_charset()
        if charset is None or len(charset) == 0:
            charsets = ['ascii', 'utf-8']
        else:
            charsets = [charset]

        part_body = part.get_payload(decode=True)
        for enc in charsets:
            try:
                part_body = part_body.decode(enc)
                break
            except UnicodeDecodeError as ex:
                continue
            except LookupError as ex:
                continue
    else:
      part_body = part.get_payload(decode=False)

    body += part_body

    if raw_message.epilogue is not None:
      body += raw_message.epilogue


    # send(forward) mail to people of selected group
    if query is not None:
      for m in query:
        emails += (
	  (
          	subject,
          	body,
        	sender,
          	[m.email,],
	  ),
	)
        self.stdout.write(self.style.NOTICE('Prepared message for <'+str(m)+'>'))

    send_mass_mail(emails)
    self.stdout.write(self.style.SUCCESS('Emails sent!'))


