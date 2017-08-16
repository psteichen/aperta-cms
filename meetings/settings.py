# Application settings for meetngs app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'         	: u'Prochaine RS',
      'icon'     	: 'plus',
      'grade'     	: 'danger',
      'url'           	: '/meetings/add/',
      'has_perms'     	: 'BOARD',
    },
    {
      'label'         	: u'Importer le Calendrier des réunions',
      'icon'          	: 'upload',
      'grade'         	: 'danger',
      'url'             : '/upload/calendar/',
      'has_perms'     	: 'BOARD',
    },
    { 
      'label'         	: u'Gestion des Lieux de Rencontre', 
      'icon'     	: 'home',
      'grade'     	: 'warning',
      'url'           	: '/locations/', 
      'has_perms'     	: 'BOARD',
    },
  ),
}

MEETINGS_TMPL_CONTENT = {
  'title'       	: u'Réunions Statutaires',
  'template'    	: 'list.html',
  'desc'       		: u'''Changement dans la tenue des Réunions Statutaires, depuis la dernière AGO (27 juin 2017) :
<ul>
  <li>Le 4ème mardi du mois, sauf juillet, août et décembre, soit 9 réunions statutaires internes au restaurant « Jardin Gourmand » à Hesperange (sauf avis contraire).</li>
  <li>S'y rajoutent 4 réunions communes pendant l’année, clubs et dates à définir. Un planning sera fixé au plus vite avec les différents clubs.</li>
</ul>
''',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'Prochaine Réunion Statutaire',
    'desc'          	: u'Ceci créé la prochaine réunion statutaire et prépare les invitations à envoyer.',
    'submit'   		: u'Ajouter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouvelle Réunion Statutaire créée',
      'message'     	: u'''
<pre>
Message d'invitation: 
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
    'desc'          	: u'Envoie ou renvoie les invitations pour la réunion statutaire choisie, par e-mail.',
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
  'invite': {
    'template'		: 'multiform.html',
    'title'     	: u'Invité(s) pour la ',
    'desc'          	: u'Chaque membre peu inviter jusqu\'à 3 personnes par réunion statutaire :',
    'submit'   		: u'Inviter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invité(s) enregistré(s)',
      'message'     	: u'''
<pre>
Message d'invitation: 
--------------------------------------
%(email)s
--------------------------------------

Destinataires: 
%(list)s
</pre>
''',
      'email': {
	'template'	: 'meeting_invitation_invitee.txt',
	'subject'	: u'[51 aperta] %(title)s',
      },
    },
  },
  'modify' : {
    'template'  	: 'form.html',
    'title'           	: u'Modifier la {meeting}',
    'desc'            	: u'Modifier les détails d\'une réunion statutaire.',
    'submit'            : u'Enregistrer',
    'done' : {
      'template'        : 'done.html',
      'title'           : u'La [{meeting}] a été modifiée!',
      'message'       	: u'',
    },
  },
  'details': {
    'template'  	: 'done.html',
    'title'     	: u'Détail de la %(meeting)s',
    'overview' : {
      'template'	: 'overview_meeting.html',
      'modify'		: u'Modifier',
      'date'		: u'Date et heure',
      'attach'		: u'Informations supplémentaires',
      'location'	: u'Lieu de rencontre',
      'report'		: u'Compte rendu',
      'listing'		: u'Listing pour PV',
      'attendance'	: u'Présent(s)',
      'invitee'		: u'Invité(s)',
      'excused'		: u'Excusé(s)',
    },
  },
  'report': {
    'template'		: 'form.html',
    'title'         	: u'Compte rendu de la Réunion Statutaire n° {0}',
    'desc'          	: u'Enregistre le compte rendu de la réunion statutaire choisie et si voulu, envoi ce dernier à tous le membres après téléchargement.',
    'submit'   		: u'Enregistrer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Compte rendu enregistré.',
      'title_send'     	: u'Compte rendu enregistré et envoyé aux membres.',
      'message'     	: u'',
      'message_send'   	: u'Destinataires : ',
      'email': {
	'template'	: 'meeting_report.txt',
	'subject'	: u'[51 aperta] Compte rendu de la %(title)s',
      },
    },
  },
  'listing': {
    'template'  	: 'done.html',
    'title'     	: u'Listing (district) de la %(meeting)s',
    'content' : {
      'template'	: 'listing_meeting.html',
      'date'		: u'Date et heure',
      'location'	: u'Lieu de rencontre',
      'members'		: u'',
      'invitee'		: u'Invités',
      'resume'		: u'',
    },
  },
}

