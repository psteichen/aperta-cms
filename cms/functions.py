from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################

def notify_by_email(sender,to,subject,message_content,template='default.txt',attachment=None):

  if not sender: sender = settings.EMAILS['sender']['default']
  email = EmailMessage(
                subject=subject,
                from_email=sender,
                to=[to],
#                cc=[settings.TEMPLATE_CONTENT['email']['cc'][int(dept)]]
          )
  message_content['FOOTER'] = settings.EMAILS['footer']
  email.body = render_to_string(template,message_content)
  if attachment: email.attach(attachment)
  try:
    email.send()
    return True
  except:
    return False

def show_form(wiz,step,field,const):
  cleaned_data = wiz.get_cleaned_data_for_step(step) or {}
  d = cleaned_data.get(field) or 666
  return int(d) == const

