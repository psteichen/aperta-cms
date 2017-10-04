# Application settings for locatins app
# coding=utf-8

ACTIONS = {
  'main' : (
    { 
      'label'         	: 'Ajouter', 
      'icon'     	: 'plus',
      'grade'     	: 'danger',
      'url'           	: '/locations/add/', 
      'has_perms'     	: 'cms.COMM',
    },
  ),
}

LOCATIONS_TMPL_CONTENT = {
  'title'       	: u'Lieux de Rencontres et d\'Activités',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'         	: u'Ajouter un Lieu de Rencontres', 
    'desc'          	: u'Ajouter un Lieu de Rencontres (restaurant ou autre).', 
    'submit'   		: u'Nouveau lieu de rencontres',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouveau lieu de rencontres créé.',
      'message'     	: u'Détails ci-dessous: ',
    },
  },
  'modify' : {
    'template'		: 'form.html',
    'title'         	: 'Modifier "%(location)s"',
    'desc'          	: 'Modifier les détails d\'un lieu de rencontre.',
    'submit'           	: 'Soumettre',
    'done' : {
      'template'       	: 'done.html',
      'title'         	: u'Le Lieu de Rencontres "%(location)s" a été modifié.',
      'message'       	: u'',
    },
  },
  'contact' : {
    'add' : {
      'title'         	: u'',
      'submit'         	: 'soumettre',
      'done' : {
        'template'     	: 'done.html',
        'title'        	: u'',
      },
    },
  },
}

