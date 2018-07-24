# Application settings for events app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'           : u'Ajouter un évènement',
      'icon'            : 'plus',
      'grade'           : 'danger',
      'url'             : '/events/add/',
      'has_perms'       : 'BOARD',
    },
  ),
}

EVENTS_TMPL_CONTENT = {
  'title'       	: u'Évènements',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'calendar': {
    'template'          : 'done.html',
    'title'             : u'Calendrier des évènements',
    'overview' : {
      'template'        : 'overview_events-calendar.html',
      'register'        : u"S'enregistrer",
      'view'        	: u"S'informer",
    },
  },
  'add': {
    'template'		: 'form.html',
    'title'     	: u'Créer un évènement',
    'desc'     		: u'Ceci créé un évènement et prépare les invitations à envoyer.',
    'submit'   		: u'Ajouter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouvel évènement créé:',
      'message'     	: u'''
<div class="well">
<h3>Titre : {event.title}</h3>
<h4>Date : {event.when}</h4>
<h4>Lieu : {event.location}</h4>
<h4>Information(s) supplémentaire(s) :</h4>
<p>{message}</p>
<p><a href="/media/{attachement}" target="_blank">Voire les annexes</a></p>
<hr />
<h5>Club(s) partenaire(s) :</h5>
<ul>{partners}</ul>
<h5>Les invité(e)s :</h5>
<ul>{invitees}</ul>
</div>
''',
    },
  },
  'send': {
    'template'		: 'form.html',
    'title'     	: u'(R)Envoyer Invitations',
    'desc'              : u'Envoie ou renvoie les invitations pour l\'évènement choisie, par e-mail.',
    'submit'            : u'Envoyer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations pour la : %s envoyées',
      'message'         : u'Destinataires : ',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: u'%(title)s',
      },
    },
  },
  'register': {
    'template'          : 'events_reg.html',
    'title'             : u'{}',
    'header'            : u"Formulaire d'inscription :",
    'submit'            : u"S'inscrire",
    'teaser' : {
      'template'        : 'teaser_event_reg.html',
      'title'           : u"Détails de l'évènement :",
      'date'            : u'Date',
      'location'        : u'Lieu',
      'agenda'          : u'Agenda',
      'info'            : u'Informations supplémetaires',
    },
    'email': {
      'template'        : 'event_registration.txt',
      'subject'         : u'Merci pour votre inscription',
    },
    'done': {
      'template'        : 'done.html',
      'title'         	: u'Merci pour votre inscription à notre évènement : {}',
      'overview' : {
        'template'      : 'overview_event_reg.html',
        'date'          : u'Date and heure de début',
        'location'      : u'Lieu',
        'agenda'        : u'Agenda',
        'info'          : u'Informations supplémetaires',
        'regcode'       : u"Votre code d'accès :",
      },
    },
  },
  'modify' : {
    'template'		: 'form.html',
    'title'             : u'Modifier un Evènement',
    'desc'              : u'Modifier les détails et les présences d\'un évènement.',
    'submit'   		: u'Ajouter',
    'done' : {
      'template'        : 'done.html',
      'title'           : u"L'évènement <i>{event}</i> a été modifiée!",
    },
  },
  'details': {
    'template'          : 'done.html',
    'title'             : u'Détail de l\'évènement %(event)s',
    'overview' : {
      'template'        : 'overview_event.html',
      'modify'          : u'Modifier',
      'date'            : u'Date et heure',
      'location'        : u'Lieu de rencontre',
      'agenda'          : u'Agenda',
      'invitation'      : u"Texte de l'Invitation",
      'attachement'     : u'Informations supplémentaires',
      'attendance'      : u'Liste des inscrits',
      'registration'    : u"Lien d'inscription",
    },
  },
}
