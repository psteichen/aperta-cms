# Application settings for locatins app
# coding=utf-8

ACTIONS = {
  'main' : (
    { 
      'label'         	: 'Ajouter', 
      'icon'     	: 'plus',
      'url'           	: '/locations/add/', 
      'has_perms'     	: 'cms.COMM',
    },
  ),
}

LOCATIONS_TMPL_CONTENT = {
  'title'       	: 'Gestions de Lieux de Rencontres',
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
    'first'           	: 'début',
    'prev'            	: 'retour',
    'location' : {
      'title'         	: u'Modifier un Lieu de Rencontres',
      'desc'         	: u'Modifier les détails d\'un Lieu de Rencontres',
      'next'          	: 'suite',
    },
    'contact' : {
      'title'         	: u'Modifier le Contact',
      'desc'         	: u'Modifier les détails de la personne de Contact',
      'next'          	: 'soumettre',
    },
    'done' : {
      'template'      	: 'done.html',
      'title'         	: u'Lieu de Rencontres [%s] a été modifié!',
    },
  },
}

