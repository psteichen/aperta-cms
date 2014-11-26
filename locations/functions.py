from django.conf import settings
from django.template.loader import render_to_string


##################################
# LOCATIONS SUPPORTING FUNCTIONS #
##################################

def gen_contact_initial(c):
  initial_data = {}

  initial_data['first_name'] = c.first_name
  initial_data['last_name'] = c.last_name
  initial_data['tel'] = c.tel
  initial_data['mobile'] = c.mobile
  initial_data['email'] = c.email

  return initial_data

def gen_location_initial(l):
  initial_data = {}

  initial_data['name'] = l.name
  initial_data['address'] = l.address
  initial_data['tel'] = l.tel
  initial_data['email'] = l.email
  initial_data['website'] = l.website
  initial_data['contact'] = l.contact

  return initial_data


