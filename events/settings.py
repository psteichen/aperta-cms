# Application settings for events app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choose actions on <strong>events</strong>:',
    'has_perms'         : 'cms.BOARD',
    'actions'   : (
      {
        'label'         : 'Add Event',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Add a new meeting',
        'url'           : '/events/add/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : 'Send Event Invitations',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Send Invitations (or reminder) for a specified event.',
        'url'           : '/events/send/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : 'Modify Event',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Modify a meeting',
        'url'           : '/events/modify/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : 'List Events',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'List all events',
        'url'           : '/events/list_all/',
    	'has_perms'     : 'cms.BOARD',
      },
    ),
  },
  {
    'has_perms'         : 'cms.BOARD',
    'actions'   : (
      { 
        'label'         : 'Location Management', 
        'glyphicon'     : 'glyphicon-home',
        'desc'          : 'Add a Location.', 
        'url'           : '/locations/', 
    	'has_perms'     : 'cms.BOARD',
      },
    ),
  },
)

EVENTS_TMPL_CONTENT = {
  'title'       : 'Event Management',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
  'add': {
    'template'	: 'form.html',
    'title'     : ACTIONS[0]['actions'][0]['desc'],
    'desc'     	: 'Create Event & Send Invitations',
    'submit'   	: 'GO',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Event added',
      'message'     	: '''
<pre>
Invitation e-mail: 
--------------------------------------
%(email)s
--------------------------------------

Recipients: 
%(list)s
</pre>
''',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: '[51 aperta] %(title)s',
      },
    },
  },
  'send': {
    'template'	: 'form.html',
    'title'     : ACTIONS[0]['actions'][1]['label'],
    'desc'     	: ACTIONS[0]['actions'][1]['desc'],
    'submit'   	: 'GO',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'Invitations Event: %s',
      'message'     	: 'Sent to: ',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: '[51 aperta] %(title)s',
      },
    },
  },
  'attendance': {
    'template'	: 'done.html',
    'title'     : u'Participation à la %(meeting)s',
    'too_late' 	: u'Désolé il est <strong>trop tard</strong> pour s\'inscrire/désister!',
    'yes'  	: u'%(name)s, par la présente ta <strong>participation</strong> est <strong>confirmé(e)</strong>!',
    'no'  	: u'%(name)s, merci de nous avoir notifier ton désistement, tu sera <strong>excusé(e)</strong>!',
    'email' : {
      'yes'	: u'''
Par la présente ta participation à la %(meeting)s est confirmé(e)!''',
      'no'  	: u'''
Merci de nous avoir notifier ton désistement, pour la %(meeting)s. 

Tu sera excusé(e).''',
    },
  },
  'list_all': {
    'template'  : 'list.html',
    'title'     : 'Liste des réunions',
    'desc'     	: ACTIONS[0]['actions'][3]['desc'],
  },
  'list': {
    'template'  : 'done.html',
    'title'     : u'Détail de l\'événement "%(event)s"',
    'overview' : {
      'template'	: 'overview_event.html',
      'date'		: u'Date et heure',
      'location'	: u'Lieu',
      'attendance'	: u'Présent(s)',
      'excused'		: u'Excusé(s)',
    },
  },
  'modify' : {
    'title'     : ACTIONS[0]['actions'][2]['label'],
    'first'	: 'first',
    'prev'	: 'back',
    'list' : {
      'title'   : 'Choose Event to modify',
      'next'    : 'next',
    },
    'meeting' : {
      'title'   : 'Modify Event',
      'next'    : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Event [%s] modified!',
    },
  },
}

