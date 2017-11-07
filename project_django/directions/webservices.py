# -*- coding: utf-8 -*-

from requests import get, HTTPError
from re import sub
import datetime


# Django et Python n'importent pas de la meme facon les modules.
# Il faut donc differencier deux facons d'importer, une qui servira au lancement de Django
# Et une autre pour l'execution des fichiers Python
try:
    from directions import definition_exceptions
except ModuleNotFoundError:
    import definition_exceptions


# Liste des cles d'API necessaires a leur fonctionnement
GOOGLE_KEY = 'AIzaSyCq64SBYC4TlMFNODwtm3D3XXcBsNoNpDw'
GOOGLE_KEY_SECOURS = 'AIzaSyBbGFsuZ4lz4BsamY8nMiUH3HLGomwIZmU'
WEATHER_KEY = "f3904bf691d361bae156a10d1ab0fc93"



class WebServices:


    def _communication(self, url, key=""):
        """Recupere un json dans la réponse de l'API"""
        resp = get(url + key)

        # Permet de verifier qu'une reponse est bien obtenue
        if resp.status_code != 200:
            raise HTTPError('GET /tasks/ {}'.format(resp.status_code))

        result = resp.json()
        return result


# Dans les classes ci-dessous, il n'y a pas d'attributs stockés.
# Les méthodes sont utilisées dans les classes de classess_trajet, c'est pourquoi nous ne les protégeons pas.


class GoogleClass(WebServices):
    """Definit les differents services internet de Google qui vont être nécessaires"""


    def get_etapes_and_time(self, departure, arrival, mode):
        """Obtenir les directions et le temps du trajet"""

        # Vérifie le type des arguments
        arrival = arrival.encode('utf8').decode()
        departure = departure.encode('utf8').decode()

        if not isinstance(departure, str):
            raise TypeError("Le departure doit etre une chaine de caracteres")
        if not isinstance(arrival, str):
            raise TypeError("Le arrival doit etre une chaine de caracteres")
        if not isinstance(mode, str):
            raise TypeError("Le nom doit etre une chaine de caracteres")

        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ departure + '&language=fr'+'&destination='+ arrival + '&region=fr' + '&mode=' + mode + '&key='

        result = self._communication(url, GOOGLE_KEY)

        # Quota d'appel à l'API Google Maps atteint pour la clé, il faut en changer
        if result.get("status") == 'OVER_QUERY_LIMIT':
            result = self._communication(url, GOOGLE_KEY_SECOURS)
            if result.get("status") == 'OVER_QUERY_LIMIT':
                raise definition_exceptions.QuotaAtteint("Changez de clé d'API, la limite a été atteinte avec celles disponibles (pour aujourd'hui)")


        # GET ETAPES
        # Nettoie les directions de caracteres speciaux
        expression = r'<[^>]*>'
        directions = [element.get('html_instructions') for element in result.get('routes')[0].get('legs')[0].get('steps')]
        directions_propres = [sub(expression,"",element) for element in directions]


        # GET_TIME
        # Si le status est ZERO_RESULTS cela indique qu'aucun itinéraire n'a pu être identifié
        # On va alors essayer de lever une erreur précisant à l'utilisateur d'où provient cette absence d'itineraire trouvé
        if result.get("status") == 'ZERO_RESULTS':

                if 'partial_match' in result.get("geocoded_waypoints")[0].keys():
                    if result.get("geocoded_waypoints")[0]['partial_match']:
                        raise definition_exceptions.ItineraireNonTrouve("Essayez de préciser l'adresse de départ")

                if 'partial_match' in result.get("geocoded_waypoints")[1].keys():
                    if result.get("geocoded_waypoints")[1]['partial_match']:
                        raise definition_exceptions.ItineraireNonTrouve("Essayez de préciser l'adresse d'arrivée")

                if 'street_address' not in result.get("geocoded_waypoints")[0]['types']:
                    raise definition_exceptions.ItineraireNonTrouve("L'adresse de depart n'est pas reconnue comme une adresse de rue")

                if 'street_address' not in result.get("geocoded_waypoints")[1]['types']:
                    raise definition_exceptions.ItineraireNonTrouve("L'adresse d'arrivee n'est pas reconnue comme une adresse de rue")

                raise definition_exceptions.ItineraireNonTrouve("Itineraire non trouvé par GoogleMaps")


        temps_text = result.get('routes')[0].get('legs')[0].get('duration').get('text')

        # Convertir le temps obtenu qui est sous forme de texte en élèments utilisables
        temps = temps_text.split(" ")

        # Commençons par les jours
        if "jours" in temps:
            day = temps[temps.index("jours") -1]
        elif "jour" in temps:
            day = temps[temps.index("jour") -1]
        else:
            day=0

        # Puis les heures
        if "heures" in temps:
            hour = temps[temps.index("heures") - 1]
        elif "heure" in temps:
            hour = temps[temps.index("heure") - 1]
        else:
            hour = 0

        # Puis les minutes
        if "minutes" in temps:
            minute = temps[temps.index("minutes") - 1]
        elif "minute" in temps:
            minute = temps[temps.index("minute") - 1]
        else:
            minute = 0

        time = datetime.timedelta(minutes= int(minute), hours=int(hour), days=int(day))

        return directions_propres, time


    def get_info_adresse(self,address):
        """Transforme une adresse pour la convertir en coordonnees de geolocalisation"""

        address.replace(" ", "+")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"+&key="
        result = self._communication(url, GOOGLE_KEY)

        # Quota d'appel à l'API Google Maps atteint pour la clé, il faut en changer
        if result.get("status") == 'OVER_QUERY_LIMIT':
            result = self._communication(url, GOOGLE_KEY_SECOURS)
            if result.get("status") == 'OVER_QUERY_LIMIT':
                raise definition_exceptions.QuotaAtteint("Changez de clé d'API, la limite a été atteinte avec celles disponibles (pour aujourd'hui)")

        # Si aucun  resultat n'est trouve par Google, il ne renverra pas de resultat, ce qu'il faudra signaler.
        if len(result.get('results')) == 0:
            raise definition_exceptions.AdresseNonComprise("Google ne trouve pas l'adresse")


        coord = result.get('results')[0].get('geometry').get('location')
        adresse_format = result.get("results")[0].get("formatted_address")

        # Verifie que les coordonnées du lieu designent bien un lieu dans Paris
        if coord['lng'] < 2.241803 or coord['lng'] > 2.430441:
            raise  definition_exceptions.AdresseHorsParis("L'adresse '{}' ne semble pas se trouver à Paris".format(address))
        if coord['lat'] < 48.813377 or coord['lat'] > 48.908506:
            raise definition_exceptions.AdresseHorsParis("L'adresse '{}' ne semble pas se trouver à Paris".format(address))

        return [(coord['lat'], coord['lng']), adresse_format]


class WeatherClass(WebServices):
    """Definit la classe qui va appeler les services meteo"""
    def __init__(self, city):
        self.city = city

    def does_it_rain(self):
        """Permet de savoir si les conditions meteos sont bonnes"""
        url="http://api.openweathermap.org/data/2.5/weather?q="+self.city+",fr&APPID="

        result = self._communication(url, WEATHER_KEY)

        #if 'weather' not in result.keys():

        raise definition_exceptions.MeteoBroken("L'appel à l'API Météo n'a pas marché (nombre de requête trop important ou erreur réseau)")

        meteo = result.get('weather')[0].get('description')

        bad_conditions = ["shower rain", "rain", "thunderstorm", "snow", "mist"]
        traduction_fr = {"few clouds":"Quelques nuages","scattered clouds":"Nuageux","broken clouds":"Très nuageux","clear sky":"ciel dégagé","shower rain":"Forte pluie", "rain":"Pluie", "thunderstorm":"Orage", "snow":"Neige", "mist":"Innondations"}

        if meteo in bad_conditions:
            return traduction_fr[meteo],True
        else:
            return traduction_fr[meteo],False


class OpendataParisClass(WebServices):
    """Definit les appels a l'OpenData de la ville de Paris pour obtenir des informations sur les Velibs et Autolibs
    Les informations seront traitees dans le fichier des classes Velibs et Autolibs"""

    def __init__(self):
        pass

    def call_opendata(self,lat,lng,radius,dataset):
        """Recupere les informations de l'open data en fonction de parametres geographiques"""
        url="https://opendata.paris.fr/api/records/1.0/search/?dataset="+dataset+"&geofilter.distance="+str(lat)+"%2C"+str(lng)+"%2C"+str(radius)
        return self._communication(url)

if __name__ == '__main__':
    test = GoogleClass()
    print(test.get_info_adresse("10 rue Tolbiac"))
