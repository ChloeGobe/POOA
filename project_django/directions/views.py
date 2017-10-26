from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from directions.classes_trajet import *
from directions.webservices import WeatherClass
import json

def index(request):

    template = loader.get_template('index.html')
    depart = "123 rue Saint Jacques Paris"
    arrivee = "5 avenue de paris Boulogne"
    context = {"futur_place" : arrivee, "current_place" : depart}

    return render(request, 'index.html', context)

def results(request):
    if request.method == 'POST':
        content = json.dumps(request.POST)
        content = json.loads(content)
        depart = "123 rue Saint Jacques Paris"
        arrivee = "5 avenue de paris Boulogne"
        depart = content['depart']
        arrivee = content['arrivee']
        depart =str(depart)
        arrivee = str(arrivee)
        print(depart)
        print(arrivee)
        # Gestion de la pluie en A
        weather = WeatherClass(depart)
        #bad_conditions = weather.does_it_rain()
        trajet_metro = Metro(depart, arrivee)
        trajet_autolib = Autolib(depart, arrivee)
        trajets = [trajet_metro, trajet_autolib]

        #if not bad_conditions:
        trajet_a_pied = Pieton(depart, arrivee)
        trajet_velib = Velib(depart, arrivee)
        trajets += [trajet_a_pied, trajet_velib]

        trajet_min = trajet_autolib

        for i in trajets:
            if i.temps_trajet < trajet_min.temps_trajet:
                trajet_min = i

        nomTrajet = trajet_min.__class__.__name__
        print("Le meilleur trajet est " + trajet_min.__class__.__name__ + " avec un temps de " + str(trajet_min.temps_trajet))
        print("Etapes a suivre:\n")
        for elem in trajet_min.etapes_iti:
            print(elem)

        return render(request, 'results.html', {'trajet_min': trajet_min})
