# coding=utf-8
"""
Django settings for cms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os import path
BASE_DIR = path.dirname(path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i7_hpg!p406zhnei*v6(v+bm@rav4(r!)090re3df52o9b71c1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [ 'dev.cms.aperta.lu', ]

# Application definition

INSTALLED_APPS = (
# django core apps
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
# specific supporting apps
  'django_tables2',
  'breadcrumbs',
# my apps
  'cms',
  'members',
  'locations',
  'attendance',
  'meetings',
  'events',
  'selling',
  'webcontent',
)

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
# via supporting apps
  'breadcrumbs.middleware.BreadcrumbsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.core.context_processors.tz',
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.request', #needed for django-tables2
  'cms.context_processors.template_content',
)

ROOT_URLCONF = 'cms.urls'

WSGI_APPLICATION = 'cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': path.join(BASE_DIR, 'cms/db.sqlite'),
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/Luxembourg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (
    path.join(BASE_DIR, 'cms/static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Media files (use uploaded documents)
#MEDIA_ROOT =  '/var/www/aperta.lu/www/files/'
MEDIA_ROOT =  '/Users/pst/Projects/APERTA/media/'
MEDIA_URL =  'https://aperta.lu/files/'

# LOCAL settings

APP_ENV='DEV'

#login/auth (used by the login_required decorator)
LOGIN_URL="/login/"
LOGIN_REDIRECT_URL="/"

#where to find templates
TEMPLATE_DIRS = (
  path.join(BASE_DIR, 'cms/templates/'),
  path.join(BASE_DIR, 'cms/templates/email/'),
)

#emails
EMAILS = {
  'sender' : {
    'default'	: 'board@aperta.lu',
  },
  'footer' 	: '''
Amicalement,
Le comité APERTA
''',
}

#content for templates and views
TEMPLATE_CONTENT = {
  #basic/generic content for all templates/views:
  'meta' : {
    'author'            : 'Pascal Steichen - pst@aperta.lu',
    'copyright'         : 'FIFTY-ONE Luxembourg APERTA a.s.b.l.',
    'title'             : 'Club Management System',
    'logo' : {
      'title'		: 'FIFTY-ONE<br/>Luxembourg<br/><strong><em>aperta</em></strong>',
      'img'		: 'http://aperta.lu/pics/logo-51-aperta_picto.png',
    },
    'description'       : '',
    'keywords'          : '',
    'css' : {
        'bt'            : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css',
        'bt_theme'      : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css',
        'own'           : STATIC_URL + 'css/bt-aperta.css',
        'dtpicker'      : STATIC_URL + 'css/jquery.datetimepicker.css',
#        'dtpicker'      : 'https://raw.githubusercontent.com/xdan/datetimepicker/master/jquery.datetimepicker.css',
    },
    'js' : {
        'bt'       	: 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js',
        'jq'		: 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js',
        'dtjq'		: STATIC_URL + 'js/jquery.js',
        'dtpicker'      : STATIC_URL + 'js/jquery.datetimepicker.js',
#        'dtpicker'      : 'https://raw.githubusercontent.com/xdan/datetimepicker/master/jquery.datetimepicker.js',
    },
  },
  'error' : {
    'gen'               : 'Error in input validation!',
    'email'             : 'Error in email notification!',
    'no-data'           : 'No data!',
    'duplicate'         : 'Duplicate found, reconsider your input!',
    'hash'         	: 'Page not found',
  },
  'auth' : {
    'title': 'Authentication',
    'submit': 'Login',
    'chgpwd' : {
      'title': 'Change password for User: ',
      'submit': 'Change',
      'done' : {
        'title': 'Password Change completed successfully',
        'message': 'Your password has been changed successfully. Please re-login with your new credentials.',
        'backurl': '/',
        'backurl_txt': 'Back to main page.',
      },
    },
  },
}
#add env badge
try:
  TEMPLATE_CONTENT['meta']['badge'] = APP_ENV
except:
  pass

# home
ACTIONS = (
  {
    'has_perms' 	: 'cms.BOARD',
    'actions'   : (
      {         
        'label'         : u'Gestion des Réunions Statutaires', 
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Outil de gestion des réunions statutaires.',
        'url'           : '/meetings/',
    	'has_perms' 	: 'cms.BOARD',
      },
      {         
        'label'         : u'Gestion des Members', 
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Gérer les members et de leurs affiliations.',
        'url'           : '/members/',
    	'has_perms' 	: 'cms.BOARD',
      },
      {         
        'label'         : u'Gestion des Ventes', 
        'glyphicon'     : 'glyphicon-euro',
        'desc'          : 'Gérer les Produits à vendre pour une bonne cause.',
        'url'           : '/selling/',
    	'has_perms' 	: 'cms.BOARD',
      },

    ),
  },
  {
    'has_perms' 	: 'cms.COMM',
    'actions'   : (
      { 
        'label'         : 'Gestion d\'événements', 
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Gérer les actvities et événements spéciaux (hors réunions statutaires).',
        'url'           : '/events/',
    	'has_perms' 	: 'cms.COMM',
      },
      {         
        'label'         : 'Gestion du contenu en-ligne', 
        'glyphicon'     : 'glyphicon-cloud',
        'desc'          : 'Gestion et mise-à-jour du contenu du site web public.',
        'url'           : '/webcontent/',
    	'has_perms' 	: 'cms.COMM',
      },
    ),
  },
)

TEMPLATE_CONTENT['home'] = {
  'title'     	: 'What do you want to do today ?',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
}

#members
from members.settings import *
TEMPLATE_CONTENT['members'] = MEMBERS_TMPL_CONTENT

#attendance
from attendance.settings import *
TEMPLATE_CONTENT['attendance'] = ATTENDANCE_TMPL_CONTENT
ATTENDANCE_BASE_URL = 'https://' + ALLOWED_HOSTS[0] + '/attendance/'

#locations
from locations.settings import *
TEMPLATE_CONTENT['locations'] = LOCATIONS_TMPL_CONTENT

#meetings
from meetings.settings import *
TEMPLATE_CONTENT['meetings'] = MEETINGS_TMPL_CONTENT
MEETINGS_ATTENDANCE_URL = ATTENDANCE_BASE_URL + 'meetings/'

#events
from events.settings import *
TEMPLATE_CONTENT['events'] = EVENTS_TMPL_CONTENT
EVENTS_ATTENDANCE_URL = ATTENDANCE_BASE_URL + 'events/'

#selling
from selling.settings import *
TEMPLATE_CONTENT['selling'] = SELLING_TMPL_CONTENT
ORDER_URL = 'https://' + ALLOWED_HOSTS[0] + '/selling/order/'
ORDER_SALT = 'vHJe$43%e"G'
ORDER_IMAGE_DIR = path.join(MEDIA_ROOT,'products')

#webcontent
#from webcontent.settings import *
#TEMPLATE_CONTENT['webcontent'] = WEBCONTENT_TMPL_CONTENT

