# Django et Python n'importent pas de la meme facon les modules.
# Il faut donc differencier deux facons d'importer, une qui servira au lancement de Django
# Et une autre pour l'execution des fichiers Python
try:
    from directions import webservices
except ModuleNotFoundError:
    import webservices

import datetime



class Trajet:

    """Definit la classe trajet generale Trajet.

       Chaque trajet peut-etre decoupe en trois parties :

                1. le trajet a pied quand on quitte le lieu de depart

                2. un trajet specifique au mode de transport : velo pour le velib, la voiture pour l'Autolib, etc..
                    Ce trajet sera entre une station de depart et une station d'arrivée qui seront le lieu de départ
                    le lieu d'arrivee pour les trajets pietons et en métro

                3. le trajet a pied jusqu'au point d'arrivee"""


    def __init__(self, lieu_depart, lieu_arrivee):
        self.lieu_depart = lieu_depart
        self.lieu_arrivee = lieu_arrivee


    def get_trajet_specifique(self):
        """Calcule le trajet specifique a l'aide de Google Maps Directions"""
        web_services = webservices.GoogleClass(self._station_depart, self._station_arrivee, self.mode)

        # Resume dans un dictionnaire les differentes etapes du trajet et son temps total
        summary = {
            'duration': web_services.get_time(),
            "etapes": web_services.get_etapes(),
        }

        return summary


    def get_trajet_total(self):
        """Somme les differents bouts de trajet pour completer l'objet trajet avec le temps de trajet total et les etapes"""

        # 1ere etape : se rendre à une station de depart s'il y en a une (sinon station_depart est le lieu de depart)
        etapeA= Pieton(self.lieu_depart, self._station_depart).get_trajet_specifique()

        # 2eme etape : faire le trajet spécifique : vélo, auto, ...
        etapeB = self.get_trajet_specifique()

        # 3eme etape : se rendre à la station d'arrivee s'il y en a une (sinon station_arrivee est le lieu d'arrivee)
        etapeC = Pieton(self._station_arrivee, self.lieu_arrivee).get_trajet_specifique()

        # Si l'étape piétonne est trop brève (la station est proche), nul besoin de la compter,
        # elle sera reprise dans une autre etape par Google maps
        if etapeA['duration'] < datetime.timedelta(minutes=1) or len(etapeA["etapes"]) < 2:
            etapeA["etapes"] = ['']

        if etapeC['duration'] < datetime.timedelta(minutes=1) or len(etapeC["etapes"]) < 2:
            etapeC["etapes"] = ['']

        summary = {
            "duration": etapeA["duration"] +
                        etapeB["duration"] +
                        etapeC["duration"]
            ,
            # Les precisions des differentes etapes pourront être enlevees après l'etape de developement
            "etapes" : [etapeA["etapes"],etapeB["etapes"],etapeC["etapes"]]
        }
        return summary


    @property
    def etapes_iti(self):
        return self.get_trajet_total()["etapes"]

    @property
    def temps_trajet(self):
        return self.get_trajet_total()["duration"]

    @property
    def mode(self):
        if self._mode.lower() in ["walking", 'driving', 'transit', "bicycling"]:
            return self._mode.lower()

    @property
    def station_depart(self):
        return self._station_depart



class Pieton(Trajet):
    """Definit les trajets a pied.
    La classe est utilisee pour un trajet a pied mais aussi pour des portions de trajet realises avec un moyen de transport different."""

    def __init__(self, lieu_depart, lieu_arrivee):
        self._station_depart = lieu_depart
        self._station_arrivee = lieu_arrivee
        self._mode = "walking"
        Trajet.__init__(self, lieu_depart, lieu_arrivee)



class Metro(Trajet):
    """Definit les trajets en metro.
    Google Maps calcule le trajet dans son ensemble, marche a pied comprise.
    Le trajet en metro est considere comme etant en une seule partie"""

    def __init__(self, lieu_depart, lieu_arrivee):
        self._station_depart = lieu_depart
        self._station_arrivee = lieu_arrivee
        self._mode = "transit"
        Trajet.__init__(self, lieu_depart, lieu_arrivee)



class Location(Trajet):
    """Rassemble les locations de moyens de transport proposes par la Ville de Paris.
    Le trajet est en trois parties pour les trajets de cette classe"""

    def __init__(self,lieu_depart, lieu_arrivee):
        self._station_depart = self.__get_closest_station(lieu_depart)
        self._station_arrivee = self.__get_closest_station(lieu_arrivee)
        Trajet.__init__(self, lieu_depart, lieu_arrivee)


    @property
    def dataset(self):
        if self._dataset.lower() in ["stations-velib-disponibilites-en-temps-reel", "stations_et_espaces_autolib_de_la_metropole_parisienne"]:
            return self._dataset.lower()



    def __get_closest_station(self, address):
        """Permet d'obtenir les stations les plus proches de Velib et Autolib"""

        # Transforme une adresse en coordonnees geographiques qui vont etre utilise par l'API OpenData"
        web_services_google = webservices.GoogleClass(address, "", "walking")
        lat, lng = web_services_google.get_latlong(address)

        # Perimetre autour dans lequel on souhaite trouver nos stations
        radius = 5000
        web_services_loc = webservices.OpendataParisClass()
        resp = web_services_loc.call_opendata(lat, lng, radius, self.dataset)

        # Recupere l'adresse et l'identifiant de la station la plus proche
        closest_station_address, closest_station_name = self.get_info_station(resp)
        return closest_station_address



class Velib(Location):
    """Permet de definir les informations specifiques aux Velibs"""

    def __init__(self, lieu_depart, lieu_arrivee):
        self._dataset = "stations-velib-disponibilites-en-temps-reel"
        self._mode = "bicycling"
        Location.__init__(self, lieu_depart, lieu_arrivee)


    def get_info_station(self, reponse_webservices):
        """Recupere et selectionne les infos renvoyees par l'API pour les Velibs"""
        i = 0
        statut = reponse_webservices.get("records")[i].get("fields").get("status")

        # Tant qu'on ne trouve pas de station ouverte, on en choisit une qui est un peu plus loin
        # Les stations sont rangees par ordre de distance
        while statut != "OPEN":
            i += 1
            statut = reponse_webservices.get("records")[i].get("fields").get("status")

        adresse = reponse_webservices.get("records")[i].get("fields").get("address")
        adresse = adresse.encode('utf8')

        name = reponse_webservices.get("records")[i].get("fields").get("name")

        # Decode les informations si des bit sont renvoyes pour eviter de les transmettre a l'API Google
        if isinstance(adresse, bytes):
            adresse = adresse.decode()
        if isinstance(name, bytes):
            name = name.decode()
        return adresse, name



class Autolib(Location):
    """Permet de definir les informations specifiques aux Autolibs"""

    def __init__(self, lieu_depart, lieu_arrivee):
        self._dataset = "stations_et_espaces_autolib_de_la_metropole_parisienne"
        self._mode = "driving"
        Location.__init__(self, lieu_depart, lieu_arrivee)


    def get_info_station(self, reponse_webservices):
        """Recupere et selectionne les infos renvoyees par l'API pour les Autolibs"""

        adresse = reponse_webservices.get("records")[0].get("fields").get("adresse")
        name = reponse_webservices.get("records")[0].get("fields").get("id_autolib")

        # Decode les informations si des bytes sont renvoyes pour eviter de les transmettre a l'API Google
        if isinstance(adresse, bytes):
            adresse = adresse.decode()
        if isinstance(name, bytes):
            name = name.decode()
        return adresse, name
