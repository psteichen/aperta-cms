# Application settings for meetngs app
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
      'has_perms'     	: 'cms.COMM',
    },
  ),
}

MEETINGS_TMPL_CONTENT = {
  'title'       	: u'Réunions Statutaires',
  'template'    	: 'list.html',
  'desc'       		: u'''De manière générale les Réunions Statutaires se tiennent :
<ul>
 <li>tous les deuxièmes mardis des mois <b>pairs</b> chez ATP (Ellange) à midi,
 <li>tous les deuxièmes mardis des mois <b>impairs</b> aux Espaces Réunions (Leudelange) à midi,
 <li>tous les quatrièmes mardis de chaque mois au Jardin Gourmand (Hesperange) le soir.
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

