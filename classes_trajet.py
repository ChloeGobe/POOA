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
        etapeB = self.get_trajet_specifique()
        etapeC = Pieton(self.station_arrivee, self.lieu_arrivee).get_trajet_specifique()

        summary = {
            "duration": etapeA["duration"] + etapeB["duration"] + etapeC["duration"],
            "etapes" : etapeA["etapes"] + ["\n\n\n"] + etapeB["etapes"] + ["\n\n\n"] + etapeC["etapes"]
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
        self.mode = "walking"
        Trajet.__init__(self, lieu_depart, lieu_arrivee)




class Metro(Trajet):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.station_depart = lieu_depart
        self.station_arrivee = lieu_arrivee
        self.mode = "transit"
        Trajet.__init__(self, lieu_depart, lieu_arrivee)



class Location(Trajet):
    def __init__(self,lieu_depart, lieu_arrivee):
        self.station_depart = self.get_closest_station(lieu_depart)
        self.station_arrivee = self.get_closest_station(lieu_arrivee)
        Trajet.__init__(self, lieu_depart, lieu_arrivee)



    def get_closest_station(self, address):
        web_services_google = webservices.GoogleClass(address, "", "walking")
        lat, lng = web_services_google.get_latlong(address)
        radius = 5000
        web_services_velib = webservices.OpendataParisClass()
        resp = web_services_velib.call_opendata(lat, lng, radius, self.dataset)
        closest_station_address, closest_station_name = self.get_info_station(resp)
        return closest_station_address



class Velib(Location):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.dataset = "stations-velib-disponibilites-en-temps-reel"
        self.mode = "bicycling"
        Location.__init__(self, lieu_depart, lieu_arrivee)


    def get_info_station(self, reponse_webservices):
        i = 0
        statut = reponse_webservices.get("records")[i].get("fields").get("status")

        while statut != "OPEN":
            i += 1
            statut = reponse_webservices.get("records")[i].get("fields").get("status")

        adresse = reponse_webservices.get("records")[i].get("fields").get("address")
        adresse = adresse.encode('utf8')
        name = reponse_webservices.get("records")[i].get("fields").get("name")

        if isinstance(adresse, bytes):
            adresse = adresse.decode()
        if isinstance(name, bytes):
            name = name.decode()
        return adresse, name


class Autolib(Location):

    def __init__(self, lieu_depart, lieu_arrivee):
        self.dataset = "stations_et_espaces_autolib_de_la_metropole_parisienne"
        self.mode = "driving"
        Location.__init__(self, lieu_depart, lieu_arrivee)

    def get_info_station(self, reponse_webservices):
        adresse = reponse_webservices.get("records")[0].get("fields").get("adresse")
        name = reponse_webservices.get("records")[0].get("fields").get("id_autolib")

        if isinstance(adresse, bytes):
            adresse = adresse.decode()
        if isinstance(name, bytes):
            name = name.decode()
        return adresse, name


if __name__ == '__main__':
    depart = "123 rue Saint Jacques, Paris"
    arrivee = "32 rue de Passy, Paris"
    test = Velib(arrivee, depart)
    #print(test.station_depart)
    #print(test.station_arrivee)
    print(test.temps_trajet)
    #for i in test.etapes_iti:
    #    print(i)