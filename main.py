from  classes_trajet import Trajet

if __name__ == '__main__':
    trajet_a_pied = Trajet("Paris","Orleans")
    temps_pied = trajet_a_pied.get_temps_pied()
    print(temps_pied)
