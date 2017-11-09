Readme

<h1 align='center'> Centrale Mapper </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Projet Programmation Orientée Objet Avancée <br>
Octobre - Novembre 2017 <hr>
<u>Auteurs</u> : Eymard Houdeville, Chloé Gobé <br>
<u>Github du projet</u> : lien vers le github
</i>
<p>

## Description
<p>A partir d'une adresse de départ et d'une adresse à laquelle l'utilisateur veut se rendre, Centrale Mapper indiquera quel
est le moyen de transport qui lui est le plus adapté. Le programme prendre en compte la météo de la ville, afin d'éviter
les trajets en vélo et à pied, et si l'utilisateur indique qu'il doit transporter un objet encombrant.</p>

<p> Centrale Mapper est disponible uniquement à Paris et prend en charge les moyens de transport suivants :
    <ul>
        <li>Marche à pied</li>
        <li>Métro</li>
        <li>Velib</li>
        <li>Autolib</li>
    </ul>
</p>

## API utilisées

- Google Maps Directions : lien vers le site
- Google Maps je ne sais plus comment : lien vers le site
- OpenWeatherMaps : lien vers le site
- Open Data Paris : lien vers le site

## Requirements techniques

##### Python
- version
- librairies
    - django
    - autres installations

##### Navigateur Web
Veiller à plutôt utiliser Chrome et Firefox.
Il est conseillé dans la doc technique du service de géolocalisation de Google Maps (un module JS qui nous permet de faire des recommandations d'adresses dans la page d'accueil) de ne pas utiliser Safari.

## Contenu du projet

Arborescence du projet:

*Project_django*
- *Manage.py* est le fichier python qui permet de lancer le serveur et d'accomplir certaines opérations de bases (Django possède une base de données préintégrée).
Deux dossiers principaux structurent un projet Django:
- *pooawebsite* est le dossier "père":
  - On y trouve notamment settings.py avec les paramètres principaux de notre site
- *Directions* est l'application que nous utilisons. Techniquement ce dossier n'est pas très différent de pooawebsite. Les utilisateurs de Django recommendent généralement de segmenter un projet en plusieurs applications.
On trouve dans directions:
  - *Static*: un dossier qui contient nos templates CSS et nos images
  - *Templates*: un dossier qui comme son nom l'indique contient nos templates HTML
  - *Classes_trajet*: les objects qui permettent de calculer les itinéraires entre deux points A et B par différents moyens de transport
  - *Definition exceptions*: la gestion de nos exceptions
  - *url*: un manager d'url qui va être appelé par manage.py pour gérer les liens. Ce fichier d'url est inclu automatiquement dans le fichier global url.py que l'on trouve dans pooawebsite de sorte que Django va toujours essayer de trouver une url dans pooawebsite.urls.py avant d'aller voir dans ce fichier.
  - *Views*: nous avons défini deux vues, la vue "index" qui correspond à la page d'accueil avec son lot de variables contextuelles et la vue results pour les resultats. Les deux vues possèdent leur propre template.
  - *Webservices.py*: il s'agit du module qui gère nos différents appels aux services tiers et que nous avons préféré gardé en dehors du reste de notre code.


## Installation et lancement

##### Lancer le programme
- downloads du projet
- ligne de commande
- cd manage.py
- python manage.py runserver
=> le projet se lance normalement sur le localhost port 8000 ou 8080.
- arriver sur page index

##### Utiliser Centrale Mapper
- adresse depart et adresse arrivee, autocomplete dans Paris
- Charge ou non
- Lien vers le site de l'option ISIA
- Let's go
- Loading page + son contenu
- Page de resultat
- Meilleur moyen de transport conseillé
- Temps de trajet affiché
- Pluie ou non
- Possibilité de voir les étapes
- Etapes à pied, indication d'un changement de moyen de transport
- Retour à la recherche


## Remerciements
- Intervenants
- Mairie de Paris ?

~~~
**Notes et discussions sur la création du readme**
Chloé : Eymard, si tu penses à quelque chose que l'on doit rajouter dans le readme, on peut peut-être en discuter ici
~~~
