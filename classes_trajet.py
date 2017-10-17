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


class Metro(Trajet):

    def __init__(self, lieu_depart, lieu_arrivee):
        Trajet.__init__(self, lieu_depart, lieu_arrivee)

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

    def __init__(self,lieu_depart, lieu_arrivee):
        Trajet.__init__(self, lieu_depart, lieu_arrivee)
        self.__station_depart = self.get_closest_station(lieu_depart)
        self.__station_arrivee = self.get_closest_station(lieu_arrivee)
        self.dataset = "stations-velib-disponibilites-en-temps-reel"
        #Self.etape1 : self.get_traject_pieton()
        #etape2 : self.get_traject_velo_google()
        #etape3 : self.get_trajet_pieton()

    @property
    def get_station_arrivee(self):
        return self.__station_arrivee




    def get_closest_station(self, adresse):

        ### Transformer adresse en latitute longitude
        ## lat, long = GoogleMaps.geloc(adresse)

        radius = 5000
        web_services_velib = webservices.OpendataParisClass()
        resp = web_services_velib.call_opendata(lat, lng, radius, self.dataset)
        closest_station = resp.get("records")[0].get("fields")
        return closest_station

    # def get_trajet_velo()
    # Google








class Autolib(Trajet):

    def __init__(self, lieu_depart, lieu_arrivee):
        Trajet.__init__(self, lieu_depart, lieu_arrivee)
        self.dataset = "stations_et_espaces_autolib_de_la_metropole_parisienne"

    def get_station_autolib(self, lat, lng):
        radius = 5000
        web_services_velib = webservices.OpendataParisClass()
        resp = web_services_velib.call_opendata(lat, lng, radius, self.dataset)
        closest_station = resp.get("records")[0].get("fields")
        return closest_station


