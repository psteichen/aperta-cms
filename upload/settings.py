# Application settings for upload app
# coding=utf-8

ACTIONS = {
  'main' : (
    { 
      'label'         	: u'Importer des Membres', 
      'icon'     	: 'file',
      'grade'     	: 'danger',
      'url'           	: '/upload/members/', 
      'has_perms'	: 'cms.BOARD',
    },
    { 
      'label'         	: u'Importer le Calendrier', 
      'icon'     	: 'calendar',
      'grade'     	: 'danger',
      'url'           	: '/upload/calendar/', 
      'has_perms'	: 'cms.BOARD',
    },
  ),
}

UPLOAD_TMPL_CONTENT = {
  'title'       	: 'Membres',
  'template'  		: 'done.html',
  'actions'     	: ACTIONS['main'],
  'members': {
    'template'		: 'form.html',
    'title'     	: u'Importer des Membres',
    'desc'     		: u'''<p>L'import accepte uniquement des fichiers de type 'csv', utilisant le séparateur ";".</p>
<p>Voici un exemple :</p>
<div class="well">
PRENOM;NOM;EMAIL;ADRESSE;TEL;MOBILE</br>
Jean;Dupont;jean@dupont.lu;5, rue du Près L-1234 Mersch;36594812;621894578<br/>
...
</div>
''',
    'submit'   		: u'Importer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'{} membre(s) importé(s).',
    },
  },
  'calendar': {
    'template'		: 'form.html',
    'title'     	: u'Importer le Calendrier des réunions et/ou évènements',
    'desc'     		: u'''<p>L'import accepte uniquement des fichiers de type 'csv', utilisant le séparateur ";".</p>
<p>Voici un exemple :</p>
<div class="well">
DATE;TITRE;HEURE;TYPE;LIEU</br>
2017-09-29;Réunion statutaire;19:30;0;Fin Gourmand<br/>
2018-07-15;Fête de l'amitié du District;20:00;1;Place d'Armes</br/>
...
</div>
<p>Le TYPE définit le type de rencontre: "0" -> réunion statuaire ; "1" -> autre évènement non-statutaire.</p>
''',
    'submit'   		: u'Importer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'{} réunion(s) et/ou évènement(s) importé(es).',
    },
  }
}
