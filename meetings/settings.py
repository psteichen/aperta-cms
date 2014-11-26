# Application settings for meetngs app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : u'Choisir l\'action à faire sur les <strong>Réunions Statutaires</strong>:',
    'has_perms'         : 'cms.BOARD',
    'actions'   : (
      {
        'label'         : u'Ajouter une Réunion Statutaire',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : u'Ceci rajoute une réunion statutaire et prépare les invitations à envoyé pour cette réunion.',
        'url'           : '/meetings/add/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : u'(R)Envoyer Invitations',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : u'Envoie ou renvoie les inviations pour la réunion statutaire choisie, par e-mail.',
        'url'           : '/meetings/send/',
    	'has_perms'     : 'cms.BOARD',
      },
      {
        'label'         : u'Liste des Réunions Statutaires',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : u'Tableau des réunions enregistrer dans la base de données.',
        'url'           : '/meetings/list_all/',
    	'has_perms'     : 'cms.BOARD',
      },
    ),
  },
  {
    'has_perms'         : 'cms.BOARD',
    'actions'   : (
      { 
        'label'         : u'Gestion des Lieux de Rencontre', 
        'glyphicon'     : 'glyphicon-home',
        'desc'          : u'Gérer (ajouter/modifier) les lieux de rencontre.', 
        'url'           : '/locations/', 
    	'has_perms'     : 'cms.BOARD',
      },
    ),
  },
)

MEETINGS_TMPL_CONTENT = {
  'title'       : u'Gestion des Réunions Statutaires',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
  'add': {
    'template'	: 'form.html',
    'title'     : ACTIONS[0]['actions'][0]['label'],
    'desc'     	: ACTIONS[0]['actions'][0]['desc'],
    'submit'   	: u'Ajouter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouvelle Réunion Statutaire créée',
      'message'     	: u'''
<pre>
Invitation e-mail: 
--------------------------------------
%(email)s
--------------------------------------

Destinataires: 
%(list)s
</pre>
''',
      'email': {
	'template'	: 'meeting_invitation.txt',
	'subject'	: u'[51 aperta] %(title)s',
      },
    },
  },
  'send': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][1]['label'],
    'desc'     		: ACTIONS[0]['actions'][1]['desc'],
    'submit'   		: u'Envoyer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations pour la : %s envoyées',
      'message'     	: u'Destinataires : ',
      'email': {
	'template'	: 'meeting_invitation.txt',
	'subject'	: u'[51 aperta] %(title)s',
      },
    },
  },
  'modify' : {
    'title'         	: u'Modifier une Réunion Statutaire',
    'desc'		: u'Modifier les détails et les présences d\'une réunion statutaire.',
    'first'		: u'début',
    'prev'		: u'retour',
    'list' : {
      'title'   	: u'Choisir la réunion à modifier',
      'next'    	: 'suivant',
    },
    'meeting' : {
      'title'   	: u'Modifier la %(meeting)s',
      'next'    	: 'suivant',
    },
    'attendance' : {
      'title'   	: u'Ajuster les présences à la %(meeting)s',
      'next'    	: 'soumettre',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : u'La [%s] a été modifiée!',
    },
  },
  'list_all': {
    'template'  	: 'list.html',
    'title'    		: ACTIONS[0]['actions'][2]['label'],
    'desc'     		: ACTIONS[0]['actions'][2]['desc'],
  },
  'list': {
    'template'  	: 'done.html',
    'title'     	: u'Détail de la %(meeting)s',
    'overview' : {
      'template'	: 'overview_meeting.html',
      'modify'		: u'Modifier',
      'date'		: u'Date et heure',
      'location'	: u'Lieu de rencontre',
      'attendance'	: u'Présent(s)',
      'excused'		: u'Excusé(s)',
    },
  },

}

