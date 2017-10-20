from  classes_trajet import *
from webservices import WeatherClass

if __name__ == '__main__':

    print("Please enter point A and point B in Paris")
    depart = input("Rue A")
    arrivee = input("Rue B")

    # Gestion de la pluie en A
    weather = WeatherClass()
    good_conditions = True
    bad_conditions = ["shower rain","rain","thunderstorm","snow","mist"]

    does_it_rain = weather.get_ifit_rains(depart)
    if does_it_rain['weather']['description'] in bad_conditions:
        good_conditions = False
    else:
        good_conditions = True

    trajet_metro = Metro(depart, arrivee)
    trajet_autolib = Autolib(depart, arrivee)
    trajets = [trajet_metro, trajet_autolib]

    if good_conditions:
        trajet_a_pied = Pieton(depart, arrivee)
        trajet_velib = Velib(depart, arrivee)
        trajets.append(trajet_a_pied, trajet_velib)

    trajet_min = trajet_autolib

    for i in trajets:
        if i.temps_trajet < trajet_min.temps_trajet:
            trajet_min = i

    print("Le meilleur trajet est " + str(type(trajet_min)) + " avec un temps de " + trajet_min.temps_trajet.)
    print("Etapes a suivre:\n")
    for elem in trajet_min['etapes']:
        print(elem)
