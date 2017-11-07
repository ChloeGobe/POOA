# -*- coding: utf-8 -*-

# Django et Python n'importent pas de la meme facon les modules.
# Il faut donc differencier deux facons d'importer, une qui servira au lancement de Django
# Et une autre pour l'execution des fichiers Python
try:
    from directions import webservices
except ModuleNotFoundError:
    import webservices

import datetime


class Trajet:

    """Définit la classe trajet generale Trajet.

       Chaque trajet peut-être découpé en trois parties :

                1. le trajet à pied quand l'utilisateur quitte le lieu de départ

                2. un trajet spécifique au mode de transport : vélo pour le velib, la voiture pour l'Autolib, etc..
                    Ce trajet sera entre une station de depart et une station d'arrivée.
                    Dans le cas du Pieton et du Metro, ces stations coïncideront avec les lieux de départ et d'arrivée

                3. le trajet à pied jusqu'au point d'arrivée"""


    def __init__(self, lieu_depart, lieu_arrivee, station_depart, station_arrivee, mode):
        self._lieu_depart = lieu_depart
        self._lieu_arrivee = lieu_arrivee
        self._station_depart = station_depart
        self._station_arrivee = station_arrivee
        self._mode = mode


    def _get_trajet_specifique(self):
        """Calcule le trajet spécifique à l'aide de Google Maps Directions"""
        web_services = webservices.GoogleClass()

        # Résume dans un dictionnaire les différentes étapes du trajet et son temps total
        infos = web_services.get_etapes_and_time(self._station_depart, self._station_arrivee, self._mode)
        summary = {
            'duration':infos[1],
            "etapes": infos[0],
        }

        return summary

    def __get_trajet_total(self):
        """Somme les différents bouts de trajet pour compléter l'objet trajet avec le temps de trajet total et les étapes"""

        # 1ere étape : se rendre à une station de départ s'il y en a une (sinon station_depart est le lieu de depart)
        etapeA= Pieton(self._lieu_depart, self._station_depart)._get_trajet_specifique()

        # 2eme etape : faire le trajet spécifique : vélo, auto, ...
        etapeB = self._get_trajet_specifique()

        # 3eme etape : se rendre à la station d'arrivée s'il y en a une (sinon station_arrivée est le lieu d'arrivée)
        etapeC = Pieton(self._station_arrivee, self._lieu_arrivee)._get_trajet_specifique()

        # Si l'étape piétonne est trop brève (la station est proche), nul besoin de la compter,
        # elle sera reprise dans une autre etape par Google Maps
        if etapeA['duration'] < datetime.timedelta(minutes=1) or len(etapeA["etapes"]) < 2:
            etapeA["etapes"] = ['']

        if etapeC['duration'] < datetime.timedelta(minutes=1) or len(etapeC["etapes"]) < 2:
            etapeC["etapes"] = ['']

        # Mise en forme du résultat des étapes en mentionnant à quel moment le moyen de transport spécifique est pris.
        transition = "Prenez votre "+str(self.__class__.__name__)

        if self.__class__.__name__ == "Pieton":
            liste_etapes = [
                {"portion" : etapeA["etapes"], "methode" : "walking"},
                {"portion" : etapeB["etapes"], "methode" : self._mode},
                {"portion" : etapeC["etapes"], "methode" : "walking"}]

        else:
            liste_etapes = [
                {"portion": etapeA["etapes"], "methode": "walking"},
                {"portion" : [transition], "methode": "transition"},
                {"portion": etapeB["etapes"], "methode": self._mode},
                {"portion": etapeC["etapes"], "methode": "walking"}]

        # Résume dans un dictionnaire les différentes étapes du trajet et son temps total
        summary = {
            "duration": etapeA["duration"] +
                        etapeB["duration"] +
                        etapeC["duration"]
            ,
            "etapes" : liste_etapes
        }
        return summary


    # Les étapes de l'itinéaires sont demandées en dehors des classes, dans le view, on met donc en place un accesseur
    # Ils ne doivent néanmoins pas être modifiés à l'exterieur.
    @property
    def etapes_iti(self):
        return self.__get_trajet_total()["etapes"]

    # Les temps de trajet sont demandés en dehors des classes, dans le view, on met donc en place un accesseur.
    # Ils ne doivent néanmoins pas être modifiés à l'exterieur.
    @property
    def temps_trajet(self):
        return self.__get_trajet_total()["duration"]

    # les stations de départ et d'arrivée peuvent être obtenues par un utilisateur qui aimerait se renseigner sur ce que
    # notre site lui renvoie. Ces accesseurs ne nous sont pas utiles dans le cadre de l'exercice.
    @property
    def station_depart(self):
        return self._station_depart

    @property
    def station_arrivee(self):
        return self._station_arrivee

    # les lieux de départ et d'arrivée peuvent être obtenues par un utilisateur qui aimerait se renseigner sur ce que
    # notre site lui renvoie. Ces accesseurs ne nous sont pas utiles dans le cadre de l'exercice.
    @property
    def lieu_depart(self):
        return self._lieu_depart

    @property
    def lieu_arrivee(self):
        return self._lieu_arrivee

    # Dans le cadre de l'exercice, ces accesseurs ne nous sont pas utiles. Néanmoins, si un utilisateur extérieur veut
    # verifier quels sont les lieux de départ et d'arrivée, il pourra voir ce que Google a compris de ses input
    @property
    def lieu_depart_google(self):
        web_services_google = webservices.GoogleClass()
        adresse_google = web_services_google.get_info_adresse(self._lieu_depart)[1]
        return adresse_google

    @property
    def lieu_arrivee_google(self):
        web_services_google = webservices.GoogleClass()
        adresse_google = web_services_google.get_info_adresse(self._lieu_arrivee)[1]
        return adresse_google

    # Pour un utilisateur extérieur
    @property
    def mode(self):
        if self._mode.lower() in ["walking", 'driving', 'transit', "bicycling"]:
            return self._mode.lower()
        else:
            raise definition_exceptions.ModeNonDefini("Le mode de transport n'est pas défini dans Google Maps")




class Pieton(Trajet):
    """Définit les trajets à pied.
    La classe est utilisée pour un trajet - pied mais aussi pour des portions de trajet realisées avec un moyen de transport different."""

    def __init__(self, lieu_depart, lieu_arrivee):

        Trajet.__init__(self,
                        lieu_depart= lieu_depart,
                        lieu_arrivee=lieu_arrivee,
                        station_depart= lieu_depart,
                        station_arrivee= lieu_arrivee,
                        mode= "walking")



class Metro(Trajet):
    """Définit les trajets en metro.
    Google Maps calcule le trajet dans son ensemble, marche à pied comprise.
    Le trajet en metro est consideré comme étant en une seule partie"""

    def __init__(self, lieu_depart, lieu_arrivee):

        Trajet.__init__(self,
                        lieu_depart= lieu_depart,
                        lieu_arrivee= lieu_arrivee,
                        station_depart= lieu_depart,
                        station_arrivee= lieu_arrivee,
                        mode= "transit")



class Location(Trajet):
    """Rassemble les locations de moyens de transport proposés par la Ville de Paris.
    Le trajet est en trois parties pour les trajets de cette classe"""

    def __init__(self,lieu_depart, lieu_arrivee, dataset, mode):
        self._dataset = dataset

        Trajet.__init__(self,
                        lieu_depart= lieu_depart,
                        lieu_arrivee= lieu_arrivee,
                        station_depart= self.__get_closest_station(lieu_depart),
                        station_arrivee= self.__get_closest_station(lieu_arrivee),
                        mode= mode )



    # Pour un utilisateur
    @property
    def dataset(self):
        if self._dataset.lower() in ["stations-velib-disponibilites-en-temps-reel", "stations_et_espaces_autolib_de_la_metropole_parisienne"]:
            return self._dataset.lower()
        else:
            raise definition_exceptions.ModeNonDefini("Le mode de transport n'est pas défini dans Google Maps")


    def get_info_station(self, input):
        """Methode abstraite, elle sera définie dans les classes filles."""
        raise NotImplementedError


    def __get_closest_station(self, address):
        """Permet d'obtenir les stations les plus proches de Velib et Autolib"""

        # Transforme une adresse en coordonnees géographiques qui vont etre utilisé par l'API OpenData"
        web_services_google = webservices.GoogleClass()
        lat, lng = web_services_google.get_info_adresse(address)[0]

        # Périmetre autour  duquel on souhaite trouver nos stations
        radius = 5000
        web_services_loc = webservices.OpendataParisClass()
        resp = web_services_loc.call_opendata(lat, lng, radius, self._dataset)

        # Récupere l'adresse et l'identifiant de la station la plus proche
        closest_station_address, closest_station_name = self.get_info_station(resp)

        return closest_station_address




class Velib(Location):
    """Permet de définir les informations specifiques aux Velibs"""

    def __init__(self, lieu_depart, lieu_arrivee):
        Location.__init__(self,
                          lieu_depart= lieu_depart,
                          lieu_arrivee= lieu_arrivee,
                          dataset= "stations-velib-disponibilites-en-temps-reel",
                          mode= "bicycling")




    def get_info_station(self, reponse_webservices):
        """Récupere et sélectionne les infos renvoyées par l'API pour les Velibs"""
        i = 0
        statut = reponse_webservices.get("records")[i].get("fields").get("status")

        # Tant qu'on ne trouve pas de station ouverte, on en choisit une qui est un peu plus loin
        # Les stations sont rangeés par ordre de distance
        while statut != "OPEN":
            i += 1
            statut = reponse_webservices.get("records")[i].get("fields").get("status")

        adresse = reponse_webservices.get("records")[i].get("fields").get("address")
        adresse = adresse.encode('utf8')

        name = reponse_webservices.get("records")[i].get("fields").get("name")

        # Décode les informations si des bit sont renvoyés pour éviter de les transmettre a l'API Google
        if isinstance(adresse, bytes):
            adresse = adresse.decode()
        if isinstance(name, bytes):
            name = name.decode()
        return adresse, name



class Autolib(Location):
    """Permet de définir les informations spécifiques aux Autolibs"""

    def __init__(self, lieu_depart, lieu_arrivee):
        Location.__init__(self,
                          lieu_depart= lieu_depart,
                          lieu_arrivee= lieu_arrivee,
                          dataset="stations_et_espaces_autolib_de_la_metropole_parisienne",
                          mode= "driving")


    def get_info_station(self, reponse_webservices):
        """Récupère et sélectionne les infos renvoyées par l'API pour les Autolibs"""

        adresse = reponse_webservices.get("records")[0].get("fields").get("adresse")
        name = reponse_webservices.get("records")[0].get("fields").get("id_autolib")

        # Décode les informations si des bytes sont renvoyés pour éviter de les transmettre a l'API Google
        if isinstance(adresse, bytes):
            adresse = adresse.decode()
        if isinstance(name, bytes):
            name = name.decode()
        return adresse, name


if __name__ == '__main__':
    test = Autolib("9 rue Tolbiac", "32 rue de Passy")
    print(test.lieu_depart_google, test.lieu_arrivee_google)
