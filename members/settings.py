# Application settings for members app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choisir l\'action sur les <strong>Members</strong>:',
    'has_perms'		: 'cms.BOARD',
    'actions'   : (
      {
        'label'         : 'Ajouter un Membre',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Ceci ajoute un membre.', 
        'url'           : '/members/add/',
   	'has_perms'	: 'cms.BOARD',
      },
      {
        'label'         : 'Liste des Membres',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Tableau de tous le membres dans la base de donn√e.',
        'url'           : '/members/list/',
   	'has_perms'	: 'cms.BOARD',
      },
    ),
  },
  {
    'heading'           : 'Choose actions on <strong>roles</strong>:',
    'has_perms'		: 'cms.BOARD',
    'actions'   : (
      { 
        'label'         : 'Add Role', 
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Add a Member Role', 
        'url'           : '/members/role/add/', 
   	'has_perms'	: 'cms.BOARD',
      },
     ),
  },

)

MEMBERS_TMPL_CONTENT = {
  'title'       : 'Member Management',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
  'add': {
    'template'	: 'form.html',
    'title'     : ACTIONS[0]['actions'][0]['desc'],
    'desc'     	: '',
    'submit'   	: 'Add Member',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Member added.',
      'message'     	: 'Details here: ',
    },
  },
  'modify': {
    'title'     	: ACTIONS[0]['actions'][1]['desc'],
    'first'             : 'first',
    'prev'              : 'back',
    'overview' : {
      'title'           : 'Overview',
    },
    'list' : {
      'title'           : 'Choose Member to modify',
      'next'            : 'next',
    },
    'member' : {
      'title'           : 'Modify Member',
      'next'            : 'submit',
    },
    'role' : {
      'title'           : 'Modify Role',
      'next'            : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Member [%s] modified!',
    },
  },
  'list': {
    'template'  	: 'list.html',
    'title'     	: 'List of Members',
    'desc'     		: '',
  },
  'profile': {
    'template'  	: 'done.html',
    'title'     	: u'Profile utilisateur',
    'overview' : {
      'template'	: 'overview_member.html',
      'name'		: u'Nom',
      'username'	: u'Login',
      'email'		: u'E-mail',
      'role'		: u'R√¥le',
    },
  },
  'role' : {
    'add': {
      'template'	: 'form.html',
      'title'     	: ACTIONS[1]['actions'][0]['desc'],
      'desc'     	: '',
      'submit'   	: 'Add Member Role',
      'done': {
        'template'	: 'done.html',
        'title'     	: 'New Member Role added.',
        'message'     	: 'Details here: ',
      },
    },
  },
}
