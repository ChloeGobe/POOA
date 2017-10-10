from  classes_trajet import Trajet

if __name__ == '__main__':
    trajet_a_pied = Trajet("rue de passy","rue saint jacques")
    #moyens_de_transport = ['transit','pied']

    trajet_pieton = trajet_a_pied.get_trajet_pieton()
    trajet_transit = trajet_a_pied.get_trajet_transit()

    trajets = [trajet_pieton, trajet_transit]

    print(trajets[0])
    trajet_min = trajet_pieton
    for i in trajets:
        print(i['duration'])

        # Convertir les chaines de caract en min pour la comparaison
        if i['duration']<trajet_min['duration']:
            trajet_min = i

    print(trajet_min['mode'])
    print(trajet_min['duration'])
