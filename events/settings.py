# Application settings for events app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choisir l\'action à faire sur les <strong>Événements</strong>:',
    'has_perms'         : 'cms.BOARD',
    'actions'   : (
      {
        'label'         : 'Ajouter un Évènement',
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Ceci ajoute un évènement ou une activité et prépare les invitations/informations a envoyées aux membres.',
        'url'           : '/events/add/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : '(R)Envoyer les Invitations/Informations',
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Envoie ou renvoie les invitations/informations concernant l\'évènement ou l\'activité choisi.',
        'url'           : '/events/send/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : 'Liste des Évènements/Activités',
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Tableau des évènements/activités enregistrer dans la base de données.',
        'url'           : '/events/list_all/',
    	'has_perms'     : 'cms.BOARD',
      },
    ),
  },
  {
    'has_perms'         : 'cms.BOARD',
    'actions'   : (
      { 
        'label'         : 'Gestion des Lieux de Rencontre', 
        'glyphicon'     : 'glyphicon-home',
        'desc'          : 'Gérer (ajouter/modifier) les lieux de rencontre.', 
        'url'           : '/locations/', 
    	'has_perms'     : 'cms.BOARD',
      },
    ),
  },
)

EVENTS_TMPL_CONTENT = {
  'title'       : 'Gestion des Évènements/Activités',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
  'add' : {
    'title'     : ACTIONS[0]['actions'][0]['label'],
    'desc' 	: ACTIONS[0]['actions'][0]['desc'],
    'first'	: 'first',
    'prev'	: 'back',
    'event' : {
      'title'   : 'Ajouter un évnènenemt/une activité',
      'next'    : 'soumettre',
    },
    'location' : {
      'title'   : 'Ajouter un lieu de rencontre',
      'next'    : 'soumettre',
    },
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouvel(le) évènement/activité [%s] ajouter',
      'message'     	: u'''
<blockquote>
E-mail d'invitation/information: 
--------------------------------------
%(email)s
--------------------------------------

Destinataires: 
%(list)s
</blockquote>
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
  'list_all': {
    'template'  	: 'list.html',
    'title'     	: ACTIONS[0]['actions'][2]['label'],
    'desc'     		: ACTIONS[0]['actions'][2]['desc'],
  },
  'list': {
    'template'  	: 'done.html',
    'title'     	: u'Détail de l\'événement "%(event)s"',
    'overview' : {
      'template'	: 'overview_event.html',
      'modify'		: u'Modifier',
      'date'		: u'Date et heure',
      'location'	: u'Lieu de Rencontre',
      'invitation'	: u'Invitations',
      'sent'		: u'Envoyées le ',
      'attachement'	: u'Notice détaillée',
      'message'		: u'Message',
      'attendance'	: u'Présent(s)',
      'excused'		: u'Excusé(s)',
    },
  },
  'modify' : {
    'title'     : 'Modifier un Évènement',
    'first'	: 'first',
    'prev'	: 'back',
    'event' : {
      'title'   : 'Modifier %(event)s',
      'next'    : 'soumettre',
    },
    'attendance' : {
      'title'   : 'Ajuster les inscriptions/présences',
      'next'    : 'soumettre',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'L\'Évènement/activité [%s] a été modifié(e)!',
    },
  },
}

