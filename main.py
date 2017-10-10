from  classes_trajet import Trajet

if __name__ == '__main__':
    trajet_a_pied = Trajet("Paris","Orleans")
    #moyens_de_transport = ['transit','pied']

    trajet_pieton = trajet_a_pied.get_trajet_pied()
    trajet_transit = trajet_a_pied.get_trajet_transit()

    trajets = [trajet_pieton, trajet_transit]
    trajet_min = trajet_pieton
    for i in trajets:
        if trajet['duration']<trajet_min['duration']:
            trajet_min = i

    print(trajet_min['mode'])
    print(trajet_min['duration'])
