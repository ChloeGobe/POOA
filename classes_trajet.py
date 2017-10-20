##Classe qui definir les differents trajets
import webservices



class Trajet:
    """Definit la classe trajet generale"""
    def __init__(self, lieu_depart, lieu_arrivee):
        self.lieu_depart = lieu_depart
        self.lieu_arrivee = lieu_arrivee


    def get_trajet_specifique(self):
        web_services = webservices.GoogleClass(self.lieu_depart, self.lieu_arrivee, self.mode)
        dic = {
            'duration': web_services.get_time(),
            "etapes": web_services.get_etapes(),
        }
        return dic

    def get_trajet_total(self):
        etapeA= Pieton(self.lieu_depart, self.station_depart).get_trajet_specifique()
        etapeB = self.get_trajet_specifique(self.lieu_depart, self.lieu_arrivee, self.mode)
        etapeC = Pieton(self.station_arrivee, self.lieu_arrivee).get_trajet_specifique()

        summary = {
            "duration": etapeA["duration"] + etapeB["duration"] + etapeC["duration"],
            "etapes" : etapeA["etapes"] + etapeB["etapes"] + etapeC["etapse"]
        }
        return summary



    @property
    def etapes_iti(self):
        return self.get_trajet_total()["etapes"]

    @property
    def temps_trajet(self):
        return self.get_trajet_total()["duration"]

class Pieton(Trajet):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.station_depart = lieu_depart
        self.station_arrivee = lieu_arrivee
        self.mode = "WALKING"
        Trajet.__init__(self, lieu_depart, lieu_arrivee)




class Metro(Trajet):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.station_depart = lieu_depart
        self.station_arrivee = lieu_arrivee
        self.mode = "TRANSIT"
        Trajet.__init__(self, lieu_depart, lieu_arrivee)



class Location(Trajet):
    def __init__(self,lieu_depart, lieu_arrivee):
        self.station_depart = self.get_closest_station(lieu_depart)
        self.station_arrivee = self.get_closest_station(lieu_arrivee)
        Trajet.__init__(self, lieu_depart, lieu_arrivee)



    def get_closest_station(self, address):
        web_services_google = webservices.GoogleClass(address, "", "WALKING")
        lat, lng = web_services_google.get_latlong(address)
        radius = 5000
        web_services_velib = webservices.OpendataParisClass()
        resp = web_services_velib.call_opendata(lat, lng, radius, self.dataset)
        closest_station = resp.get("records")[0].get("fields")
        return closest_station



class Velib(Location):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.dataset = "stations-velib-disponibilites-en-temps-reel"
        self.mode = "BICYCLING"
        Location.__init__(self, lieu_depart, lieu_arrivee)


class Autolib(Location):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.dataset = "stations_et_espaces_autolib_de_la_metropole_parisienne"
        self.mode = "DRIVING"
        Location.__init__(self, lieu_depart, lieu_arrivee)



if __name__ == '__main__':
    depart = "123 rue Saint Jacques, Paris"
    arrivee = "32 rue de Passy, Paris"
    test = Metro(arrivee, depart)
    test.__dict__
