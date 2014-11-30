# coding = utf-8

import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from members.functions import get_active_members

from .models import Product

################################
# SELLING SUPPORTING FUNCTIONS #
################################

def gen_order_hash(email):
  #hash
  h = hashlib.md5()
  h.update(settings.ORDER_SALT) #salt
  h.update(unicode(email)) #message
  return unicode(h.hexdigest())

def gen_order_links(email):
  return path.join(settings.ORDER_URL, gen_order_hash(email))

def check_order_hash():
  out = {'ok': False,}

  for m in get_active_members():
    if gen_order_hash(m.email) == hash:
      out['member'] = m
      out['ok'] = True

  return out

def gen_order_initial():
  initial_data = []

  P = Product.objects.all()
  for p in P:
    data = {}
    data['product'] = p
    initial_data.append(data)

  return initial_data

def gen_receipt_message(template,order,member):
  content = {}

  content['member'] = gen_member_fullname(member)

#HERE
  content['title'] = event.title
  content['when'] = event.when
  content['time'] = event.time
  content['location'] = event.location
  content['deadline'] = event.deadline

  return render_to_string(template,content)


