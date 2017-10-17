##Classe qui definir les differents trajets
import webservices



class Trajet:
    """Definit la classe trajet generale, notamment les trajets a pied"""
    def __init__(self, lieu_depart, lieu_arrivee):
        self.lieu_depart = lieu_depart
        self.lieu_arrivee = lieu_arrivee
        self.etape_iti = []
        self.temps_trajet = 0


    def get_trajet_pieton (self):
        """Fait appel au service web Google Maps pour les trajets a pied
        Retourne un json avec le temps de trajet et les etapes de l'itineraire"""
        web_services_pied = webservices.GoogleClass(self.lieu_depart, self.lieu_arrivee, "walking")
        dic = {
            'duration' : web_services_pied.get_time(),
            "etapes" : web_services_pied.get_etapes(),
            "mode" : "WALKING"
        }
        return dic

    #Creer une classe Trajet Metro quand il s agira de raffiner les choix pour les trajets en metro
    def get_trajet_transit(self):
         """Fait appel au service web Google Maps pour les trajets en metro
        Retourne un json avec le temps de trajet et les etapes de l'itineraire"""
         web_services_metro = webservices.GoogleClass(self.lieu_depart, self.lieu_arrivee, "transit")
         dic = {
             'duration': web_services_metro.get_time(),
             "etapes": web_services_metro.get_etapes(),
             "mode" : "TRANSIT"
         }
         return dic


class Velib(Trajet):
    """Classe Velib"""
    def __init__(self, lieu_depart, lieu_arrivee):
        Trajet.__init__(self, lieu_depart, lieu_arrivee)
        self.station_depart = []
        self.station_arrivee = []

    def get_station_depart(self):
        velib_api = webservices.VelibClass()
        liste_stations = velib_api.get_stations_list()
        print(liste_stations)


if __name__ == '__main__':
    A = "123 rue Saint Jacques"
    B = "32 rue de Passy"
    test = Velib(A,B)
    test.get_station_depart()