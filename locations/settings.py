# Application settings for locatins app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choisir l\'action à faire sur les <strong>Lieux de Rencontres</strong>:',
    'has_perms'         : 'cms.COMM',
    'actions'   : (
      { 
        'label'         : 'Ajouter un Lieu de Rencontres', 
        'glyphicon'     : 'glyphicon-home',
        'desc'          : 'Ajouter un Lieu de Rencontres (restaurant ou autre).', 
        'url'           : '/locations/add/', 
    	'has_perms'     : 'cms.COMM',
      },
      {
        'label'         : 'Modifier un Lieu de Rencontres',
        'glyphicon'     : 'glyphicon-home',
        'desc'          : 'Modifier un lieu de rencontres.',
        'url'           : '/locations/modify/',
    	'has_perms'     : 'cms.COMM',
      },
      {
        'label'         : 'Liste des Lieux de Rencontres',
        'glyphicon'     : 'glyphicon-home',
        'desc'          : 'Tableau de tous les lieux de rencontres enregistrer dans la base de données.',
        'url'           : '/locations/list/',
    	'has_perms'     : 'cms.COMM',
      },
    ),
  },
)

LOCATIONS_TMPL_CONTENT = {
  'title'       	: 'Gestions de Lieux de Rencontres',
  'template'    	: 'actions.html',
  'actions'     	: ACTIONS,
  'add': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][0]['label'],
    'desc'     		: ACTIONS[0]['actions'][0]['desc'],
    'submit'   		: u'Nouveau lieu de rencontres',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouveau lieu de rencontres créé.',
      'message'     	: u'Détails ci-dessous: ',
    },
  },
  'modify' : {
    'title'     	: ACTIONS[0]['actions'][1]['label'],
    'first'           	: 'first',
    'prev'            	: 'back',
    'list' : {
      'title'         	: u'Choisir Lieu de Rencontres à modifier',
      'next'          	: 'next',
    },
    'location' : {
      'title'         	: u'Modifier un Lieu de Rencontres',
      'next'          	: 'submit',
    },
    'done' : {
      'template'      	: 'done.html',
      'title'         	: u'Lieu de Rencontres [%s] a été modifié!',
    },
  },
  'list': {
    'template'  	: 'list.html',
    'title'    		: ACTIONS[0]['actions'][2]['label'],
    'desc'     		: ACTIONS[0]['actions'][2]['desc'],
  },
}

