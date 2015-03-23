# Application settings for meetings app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'         	: u'Prochaine RS',
      'icon'     	: 'plus',
      'url'           	: '/meetings/add/',
      'has_perms'     	: 'cms.BOARD',
    },
    { 
      'label'         	: u'Gestion des Lieux de Rencontre', 
      'icon'     	: 'home',
      'url'           	: '/locations/', 
      'has_perms'     	: 'cms.BOARD',
    },
  ),
}

MEETINGS_TMPL_CONTENT = {
  'title'       	: u'Gestion des Réunions Statutaires',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'Prochaine Réunion  Statutaire',
    'desc'          	: u'Ceci créé la prochaine réunion statutaire et prépare les invitations à envoyé.',
    'submit'   		: u'Ajouter',
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
    'title'         	: u'(R)Envoyer Invitations',
    'desc'          	: u'Envoie ou renvoie les inviations pour la réunion statutaire choisie, par e-mail.',
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
  'details': {
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

