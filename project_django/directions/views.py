from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from directions.classes_trajet import *
from directions.webservices import WeatherClass
import json

def index(request):

    template = loader.get_template('index.html')

    isloaded = True
    context = {"futur_place" : arrivee,
                "current_place" : depart,
                "isloaded": isloaded}

    return render(request, 'index.html', context)

def results(request):
    if request.method == 'POST':
        print(request.POST)
        content = json.dumps(request.POST)
        content = json.loads(content)
        print(content)
        depart = content['depart']
        arrivee = content['arrivee']

        if len(depart)==0 or len(arrivee)==0:
            depart = "123 rue de Tolbiac"
            arrivee = "10 rue de Tolbiac"
        depart =str(depart)
        arrivee = str(arrivee)
        print(depart)
        print(arrivee)

        try:
            # Gestion de la pluie en A
            weather = WeatherClass(depart)
            #bad_conditions = weather.does_it_rain()

            trajet_metro = Metro(depart, arrivee)
            trajet_autolib = Autolib(depart, arrivee)
            trajets = [trajet_metro, trajet_autolib]

            #if not bad_conditions:
            trajet_a_pied = Pieton(depart, arrivee)
            trajets += [trajet_a_pied]

            if isloaded:
                trajet_velib = Velib(depart, arrivee)
                trajets += [trajet_velib]

            trajet_min = trajet_autolib
            for i in trajets:
                if i.temps_trajet < trajet_min.temps_trajet:
                    trajet_min = i

            nom_trajet = trajet_min.__class__.__name__
            etapes_trajet = trajet_min.etapes_iti
            duree_trajet = trajet_min.temps_trajet
            #resultat ={'moyen':str(nom_trajet), 'etapes':etapes_trajet, 'duree':str(duree_trajet)}
            #print(resultat)
            #print(type(resultat['etapes']))

        except: # pour le dev quand on n a pas de connection internet
            nom_trajet="mock_trajet"
            etapes_trajet=["drive to A","Walk to B","Well done you did it"]
            duree_trajet=str(datetime.timedelta(minutes=15))
            print(nom_trajet)

        return render(request, 'results.html', {'moyen':str(nom_trajet), 'etapes':etapes_trajet, 'duree':str(duree_trajet)})
