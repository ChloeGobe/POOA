# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,HttpResponseRedirect
from directions.classes_trajet import *
from directions.webservices import WeatherClass
from directions.definition_exceptions import MeteoBroken
import json

def index(request):

    loaded = False
    context = {"futur_place" : arrivee,
                "current_place" : depart,
                "loaded": loaded}

    return render(request, 'index.html', context)


def results(request):
    if request.method == 'POST':
        content = json.dumps(request.POST)
        content = json.loads(content)

        # Gestion depart et arrivee
        depart = content['depart']
        arrivee = content['arrivee']

        #Pour nos tests, si nous ne rentrons rien, adresses par défaut
        if len(depart)==0 or len(arrivee)==0:
            depart = "123 rue de Tolbiac"
            arrivee = "10 rue de Tolbiac"
        depart =str(depart)
        arrivee = str(arrivee)

        # Gestion du poids porte par l'usager: isloaded indique que ce dernier est charge
        if 'loaded' in content.keys():
            isloaded = True
        else:
            isloaded= False

        # Gestion de la pluie
        try:
            weather = WeatherClass("Paris")
            weather_like,bad_conditions = weather.does_it_rain()
        except MeteoBroken as exc:
            weather_like=exc.text
            bad_conditions=False

            pass;

        #Dans tous les cas on calcule les trajets metro et autolib

        try:
            trajet_metro = Metro(depart, arrivee)
            trajet_autolib = Autolib(depart, arrivee)
            trajets = [trajet_metro, trajet_autolib]

            # Trajet a pied depend des conditions meteo
            if not bad_conditions:
                trajet_a_pied = Pieton(depart, arrivee)
                trajets += [trajet_a_pied]

                # Trajet velib depend de la charge portee par l'utilisateur et de la méteo
                if not isloaded:
                    trajet_velib = Velib(depart, arrivee)
                    trajets += [trajet_velib]

                trajet_min = trajet_a_pied

            else:
                trajet_min = trajet_autolib
        except GoogleClassError as exc:
            erreur=

        # Calcul du trajet avec le temps de trajet minimum, parmi ceux acceptables.
        for i in trajets:
            if i.temps_trajet < trajet_min.temps_trajet:
                trajet_min = i

        nom_trajet = trajet_min.__class__.__name__

        etapes_trajet = trajet_min.etapes_iti
        duree_trajet = trajet_min.temps_trajet
        infos_trajet={'lieu_arrivee_google':trajet_min.lieu_arrivee_google,
                    'lieu_depart_google': trajet_min.lieu_depart_google,
                    'weather_like':weather_like,
                    'bad_conditions':bad_conditions,
                    'moyen':str(nom_trajet),
                    'etapes':etapes_trajet,
                    'duree':str(duree_trajet)}

        return render(request, 'results.html',infos_trajet )
    else:
        return HttpResponseRedirect('index.html')
