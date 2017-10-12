from  classes_trajet import Trajet
from webservices import WeatherClass

if __name__ == '__main__':

    print("Please enter point A and point B in Paris")
    A = raw_input("Rue A")
    B = raw_input("Rue B")

    # Gestion de la pluie en A
    weather = WeatherClass()
    does_it_rain = weather.get_ifit_rains(A)

    trajet_a_pied = Trajet(A,B)
    #moyens_de_transport = ['transit','pied']
    trajet_pieton = trajet_a_pied.get_trajet_pieton()
    trajet_transit = trajet_a_pied.get_trajet_transit()
    trajets = [trajet_pieton, trajet_transit]

    trajet_min = trajet_pieton
    for i in trajets:
        # Convertir les chaines de caract en min pour la comparaison
        if i['duration']<trajet_min['duration']:
            trajet_min = i

    print("Le meilleur trajet est " + str(trajet_min['mode']) + " avec un temps de " + str(trajet_min['duration']))
    print("Etapes a suivre:\n")
    for elem in trajet_min['etapes']:
        print(elem)
