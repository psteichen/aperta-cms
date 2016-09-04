# Application settings for members app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: u'Nouveau Membre',
      'icon'     	: 'plus',
      'grade'     	: 'danger',
      'url'           	: '/members/add/',
      'has_perms'	: 'cms.BOARD',
    },
    { 
      'label'         	: u'Importer des Membres', 
      'icon'     	: 'file',
      'grade'     	: 'warning',
      'url'           	: '/upload/members/', 
      'has_perms'	: 'cms.BOARD',
    },
    { 
      'label'         	: u'Gestion des Rôles', 
      'icon'     	: 'user',
      'grade'     	: 'info',
      'url'           	: '/members/role/', 
      'has_perms'	: 'cms.BOARD',
    },
  ),
  'profile' : (
    {
      'label'		: u'Back-office',
      'icon'     	: 'king',
      'url'           	: '/admin/',
      'has_perms'	: 'superuser',
    },
  ),
}

MEMBERS_TMPL_CONTENT = {
  'title'       	: 'Membres',
  'template'  		: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'Ajouter un Membre',
    'desc'     		: u'Ajouter un nouveau membre, would-be ou autre.',
    'submit'   		: u'Ajouter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Un nouveau Membre a été rajouté.',
      'message'     	: u'Détails : ',
    },
  },
  'import': {
    'template'		: 'form.html',
    'title'     	: u'Importer des Membres',
    'desc'     		: u"L'import peut se faire à partir d'un fichier excel ou csv.",
    'submit'   		: u'Importer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u"{nb} nouveaux membres ont été importés.",
      'message'     	: u'Détails : ',
    },
  },
  'modify': {
    'first'             : u'début',
    'prev'              : u'retour',
    'overview' : {
      'title'           : u'Résumé',
    },
    'member' : {
      'title'           : u'Modifier le Member',
      'next'            : 'enregistrer',
    },
    'mod_role' : {
      'title'           : u'Modifier le Rôle',
      'next'            : 'enregistrer',
    },
    'add_role' : {
      'title'           : u'Ajouter un rôle',
      'next'            : 'enregistrer',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Member [%s] modified!',
    },
  },
  'profile': {
    'template'  	: 'done.html',
    'actions'     	: ACTIONS['profile'],
    'title'     	: u'Profile utilisateur',
    'overview' : {
      'template'	: 'overview_member.html',
      'name'		: u'Nom',
      'username'	: u'Login',
      'email'		: u'E-mail',
      'role'		: u'Rôle',
    },
  },
  'role' : {
    'add': {
      'template'	: 'form.html',
      'title'     	: u'Ajouter un Rôle',
      'desc'     	: '',
      'submit'   	: u'Ajouter',
      'done': {
        'template'	: 'done.html',
        'title'     	: u'Un nouveau Rôle a été rajouté.',
        'message'     	: u'Détails : ',
      },
    },
  },
}
