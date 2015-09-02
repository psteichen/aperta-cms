# coding=utf-8
"""
Django settings for cms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i7_hpg!p406zhnei*v6(v+bm@rav4(r!)090re3df52o9b71c1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [ 'cms.aperta.lu', ]


# Application definition

INSTALLED_APPS = (
# global bootstrap3 integration
  'bootstrap3',
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
  'finance',
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
    'NAME': os.path.join(BASE_DIR, 'cms/db.sqlite'),
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-FR'
LC_ALL = 'fr_FR.utf8' #to be used inpython afterwards

TIME_ZONE = 'Europe/Luxembourg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'cms/static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'

# Email settings
SERVER_EMAIL = 'admin@aperta.lu'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ADMINS = (
  ('Admin', SERVER_EMAIL),
)
MANAGERS = ADMINS

# Logging
# See http://docs.djangoproject.com/en/1.7/topics/logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# LOCAL settings
from local_settings import *

#login/auth (used by the login_required decorator)
LOGIN_URL="/login/"
LOGIN_REDIRECT_URL="/"

#where to find templates
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'cms/templates/'),
  os.path.join(BASE_DIR, 'cms/templates/email/'),
)

#emails
EMAILS = {
  'sender' : {
    'default'	: "'FIFTY-ONE Aperta' <board@aperta.lu>",
  },
  'footer' 	: '''Amicalement,
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
      'title'		: 'FIFTY-ONE<br/><strong><em>APERTA</em></strong>',
      'img'		: 'https://aperta.lu/pics/logo-51-aperta_picto.png',
    },
    'description'       : '',
    'keywords'          : '',
    'favicon'		: STATIC_URL + '/favicon.ico',
    'css' : {
        'bt'      	: '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css',
        'bt_theme'      : '//maxcdn.bootstrapcdn.com/bootswatch/3.3.4/yeti/bootstrap.min.css',
        'own'           : STATIC_URL + 'css/own.css',
        'dtpicker'      : '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/css/bootstrap-datetimepicker.min.css',
    },
    'js' : {
        'jq'      	: '//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',
        'bt'       	: '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js',
        'momentjs'      : '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.3/moment-with-locales.min.js',
        'dtpicker'      : '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/js/bootstrap-datetimepicker.min.js',
    },
  },
  'error' : {
    400 : {
      'template'	: 'error400.html',
    },
    403 : {
      'template'	: 'error403.html',
    },
    404 : {
      'template'	: 'error404.html',
    },
    500 : {
      'template'	: 'error500.html',
    },
    'gen'               : u'Error dans la saisie!',
    'email'             : u'Error dans l\'envoi d\'e-mail!',
    'no-data'           : u'Pas de données!',
    'duplicate'         : u'Doublon, vérifiez votre saisie!',
  },
  'auth' : {
    'title': u'Authentification',
    'submit': u'Se connecter',
    'chgpwd' : {
      'title': u'Changer le mot de passe pour: ',
      'submit': u'Changer',
      'done' : {
        'title': u'Changement du mot de passe réussi.',
        'message': u'Ton mot de passe a été changé avec succès. Merci de te reconnecter avec le nouveau mot de passe.',
        'backurl': '/',
        'backurl_txt': u'Retour vers l\'applicaion.',
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
    'has_perms' 	: 'cms.MEMBER',
    'heading' 		: 'Association',
    'actions' : (
      {         
        'label'         : u'Réunions Statutaires', 
        'icon'     	: 'calendar',
        'desc'          : 'Outil de gestion des réunions statutaires.',
        'url'           : '/meetings/',
    	'has_perms' 	: 'cms.MEMBER',
      },
      {         
        'label'         : u'Membres', 
        'icon'     	: 'user',
        'desc'          : 'Gérer les members et leurs affiliations.',
        'url'           : '/members/',
    	'has_perms' 	: 'cms.MEMBER',
      },
      {         
        'label'         : u'Trésorerie', 
        'icon'     	: 'euro',
        'desc'          : 'Gérer les comptes et autres aspects financiers.',
        'url'           : '/finance/bank/',
   	'has_perms' 	: 'cms.BOARD',
     },

    ),
  },
  {
    'has_perms' 	: 'cms.MEMBER',
    'heading' 		: 'Activités',
    'actions'   : (
      { 
        'label'         : 'Évènements', 
        'icon'     	: 'glass',
        'desc'          : 'Gérer les actvitiés et évènements (hors réunions statutaires).',
        'url'           : '/events/',
    	'has_perms' 	: 'cms.MEMBER',
      },
      { 
        'label'        	: u'Lieux de Rencontre', 
        'icon'     	: 'home',
        'desc'         	: u'Gérer (ajouter/modifier) les lieux de rencontre.', 
        'url'          	: '/locations/', 
        'has_perms'    	: 'cms.MEMBER',
      },
#     {         
#       'label'         : 'Site web', 
#       'icon'     	: 'cloud',
#       'desc'          : 'Gestion et mise-à-jour du contenu du site web public.',
#       'url'           : '/webcontent/',
#   	'has_perms' 	: 'cms.COMM',
#     },
    ),
  },
)

TEMPLATE_CONTENT['home'] = {
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

#finance
from finance.settings import *
TEMPLATE_CONTENT['finance'] = FINANCE_TMPL_CONTENT

