from  classes_trajet import *
from webservices import WeatherClass

if __name__ == '__main__':

    print("Please enter point A and point B in Paris")
    #depart = input("Depart ?")
    #arrivee = input("Arrivee ?")
    depart = "123 rue Saint Jacques, Paris"
    arrivee = "32 rue de Passy, Paris"

    # Gestion de la pluie en A
    weather = WeatherClass(depart)
    bad_conditions = weather.does_it_rain()


    trajet_metro = Metro(depart, arrivee)
    trajet_autolib = Autolib(depart, arrivee)
    trajets = [trajet_metro, trajet_autolib]

    if not bad_conditions:
        trajet_a_pied = Pieton(depart, arrivee)
        trajet_velib = Velib(depart, arrivee)
        trajets += [trajet_a_pied, trajet_velib]

    trajet_min = trajet_autolib

    for i in trajets:
        if i.temps_trajet < trajet_min.temps_trajet:
            trajet_min = i

    print("Le meilleur trajet est " + trajet_min.__class__.__name__ + " avec un temps de " + str(trajet_min.temps_trajet))
    print("Etapes a suivre:\n")
    for elem in trajet_min.etapes_iti:
        print(elem)
