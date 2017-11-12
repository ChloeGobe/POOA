<h1 align='center'> Centrale Mapper </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Projet Programmation Orientée Objet Avancée <br>
Octobre - Novembre 2017 <hr></i></p>

__Auteurs__ : Eymard Houdeville, Chloé Gobé <br>
__Github du projet__ : `https://github.com/ChloeGobe/POOA`

## Index
1. [Description](#description)
2. [API utilisées](#api)
3. [Requirements techniques](#requirements)
4. [Contenu du projet](#arborescence)
5. [Installation et lancement](#installation)


## <a name="description"></a>1. Description
A partir d'une adresse de départ et d'une adresse à laquelle l'utilisateur veut se rendre, Centrale Mapper indiquera quel
est le moyen de transport qui lui est le plus adapté. Le programme prendre en compte la météo de la ville, afin d'éviter
les trajets en vélo et à pied, et si l'utilisateur indique qu'il doit transporter un objet encombrant.

Centrale Mapper est disponible uniquement à Paris et prend en charge les moyens de transport suivants :

* Marche à pied
* Métro
* Velib
* Autolib

## <a name="api"></a>2. API utilisées
- Google Maps Directions :  [documentation](https://developers.google.com/maps/documentation/directions/ "Title")  
- Google Maps Geocoding : [documentation](https://developers.google.com/maps/documentation/geocoding/ "Title")  
- OpenWeatherMaps : [documentation](http://openweathermap.org/current "Title")
- Open Data Paris : [documentation](https://opendata.paris.fr/api/v1/documentation "Title")
- Google Maps JavaScript (autocomplete) : [documentation](https://developers.google.com/maps/documentation/javascript/places-autocomplete)


## <a name="requirements"></a>3. Requirements techniques

##### Python
- `Python 3.6` et supérieur
- Bibliothèques à installer :
    - Django : `pip install django`
    - Requests : `pip install requests`

##### Navigateur Web recommandés
- Chrome
- Firefox

## 4. <a name="arborescence"></a>Contenu du projet : project_django


- **Manage.py** permet de lancer le serveur et d'accomplir certaines opérations de bases 
(Django possède une base de données préintégrée). <br>

-  **_pooawebsite_** est le dossier "père" contenant :
    - **settings.py** avec les configurations principales de notre site
    - **urls.py**  contenant es urls du site
    - **wsgi.py** : WGSI, littéralement "Web Server Gateway Interface" est un standart qui spécifie comment un serveur 
    web peut communiquer avec des applications web et comment des applications web peuvent être enchainées ensemble
     pour processer une requête.

- **_directions_** est l'application que nous utilisons. Techniquement ce dossier n'est pas très différent de pooawebsite.
 Les utilisateurs de Django recommendent généralement de segmenter un projet en plusieurs applications. Il contient :
    - **_templates_** contenant :
  		- *index.html* : le code HTML de notre page d'accueil
  		- *result.html* : le code HTML de notre page de résultat
   - **classes_trajet.py** : module définssant les objets qui permettent de calculer les trajets entre deux points A et B 
   par différents moyens de transport.
  - **definition_exceptions.py** : création de nos exceptions
  - **views.py** : défini deux fonctions, la vue "index" qui correspond à la page d'accueil avec son lot de variables 
  contextuelles et la vue "results" qui va effectuer les calculs pour obtenir les resultats. Les deux vues possèdent 
  leur propre template contenu dans le dossier templates.
  - **webservices.py** : module gérant les différents appels aux services tiers.
  - **apps.py** : Apps est le fichier dans lequel sont repertoriées les différentes applications django de notre projet
   (une bonne pratique consiste à segmenter un projet Django en différentes applications)
  - **urls.py** : manager d'url qui va être appelé par manage.py pour gérer les urls. 
  Ce fichier est inclu automatiquement dans le fichier global url.py que l'on trouve dans pooawebsite de sorte que Django
   va toujours essayer de trouver une url dans pooawebsite.urls.py avant d'aller voir dans ce fichier.
  - le dossier **_static_** : Une bonne pratique Django est de mettre tous les fichiers CSS et les images dans le fichier static

## <a name="installation"></a>5. Installation et lancement

### Lancer le programme
- Cloner le repository github :  `https://github.com/ChloeGobe/POOA`
- Se placer dans le dosser project django : `cd project_django`
- Taper la ligne de commande : `python manage.py runserver`
- Le serveur doit se lancer et afficher :

~~~
Performing system checks...
System check identified no issues (0 silenced).
Month DD, AAAA - HH:MM:SS
Django version 1.11.6, using settings 'pooawebsite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.~
~~~

- Ouvrir le navigateur internet : `http://localhost:8000/directions/results` ou `http://localhost:8080/directions/results`

### Utiliser Centrale Mapper

**Index**

- Taper une adresse de départ, l'autocomplete mis en place va d'abord suggérer des lieux dans Paris.
- Taper une adresse d'arrivée, l'autocomplete mis en place va d'abord suggérer des lieux dans Paris.
- Indiquer si vous portez une charge en cochant la checkbox : les trajets en vélo ne seront pas proposés.
- Cliquer sur le bouton `Let's go`

**Page d'attente**

- Votre trajet optimal est en train d'être calculé.
- Nous prenons en compte la météo à Paris pour effectuer la recommandation

**Page de resultat**

- Vous trouver affichés :
	- le temps de trajet du trajet recommandé
	- le meilleur moyen de transport conseillé
	- la météo à Paris
	- une indication d'erreur si une erreur a été detectée.
- Cliquez sur le bouton `Voir les étapes` pour obtenir les différentes étapes du trajet et les moyens de transport utilisés sur chaque portion.
- Cliquez sur le bouton `Plannifier un nouveau trajet ` pour retourner sur la page d'accueil.
