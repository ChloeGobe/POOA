
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
#Google Key de secours :

WEATHER_KEY = "f3904bf691d361bae156a10d1ab0fc93"
VELIB_KEY= "1a502a8fc4844b5414f7510e95998d40a9f02b4c"


class GoogleClass:
    """Definit les differents services internet de Google qui vont etre necessaires"""

    def __init__(self,departure,arrival,mode):

        # Verifie le type des arguments
        arrival = arrival.encode('utf8').decode()
        departure = departure.encode('utf8').decode()

        if not isinstance(departure, str):
            raise TypeError("Le departure doit etre une chaine de caracteres")
        if not isinstance(arrival, str):
            raise TypeError("Le arrival doit etre une chaine de caracteres")
        if not isinstance(mode, str):
            raise TypeError("Le nom doit etre une chaine de caracteres")
        self.departure = departure
        self.arrival = arrival
        self.duration = 0
        self.mode=mode


    def communication (self,url):
        """Recupere l'URL"""
        resp = get(url)
        return resp


    def get_etapes(self):
        """Obtenir les directions du trajet"""
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&language=fr'+'&destination='+ self.arrival + '&region=fr' + '&mode=' + self.mode + '&key='+GOOGLE_KEY

        resp = self.communication(url)

        # Permet de verifier qu'une reponse est bien obtenue
        if resp.status_code != 200:
            raise HTTPError('GET /tasks/ {}'.format(resp.status_code))
        result = resp.json()

        # Nettoie les directions de caracteres speciaux
        expression = r'<[^>]*>'
        directions = [element.get('html_instructions') for element in result.get('routes')[0].get('legs')[0].get('steps')]
        directions_propres = [sub(expression,"",element) for element in directions]
        return directions_propres


    def get_time(self):
        """Obtenir le temps de trajet"""

        # Retrieve the get
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&destination='+ self.arrival +'&mode=' + self.mode + '&key='+GOOGLE_KEY
        resp = self.communication(url)

        # Permet de verifier qu'une reponse est bien obtenue
        if resp.status_code != 200:
            raise HTTPError('GET /tasks/ {}'.format(resp.status_code))

        # Transforme le contenu en JSON
        result = resp.json()

        # Si le status est ZERO_RESULTS cela indique qu'aucun itinéraire n'a pu être identifié
        # On va alors essayer de lever une erreur précisat à l'utilisateur d'où provient cette absence d'itineraire trouve
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

                raise definition_exceptions.ItineraireNonTrouve("Itineraire non trouve par GoogleMaps")


        # Quota d'appel à l'API Google Maps atteint il faut en changer
        if result.get("status") == 'OVER_QUERY_LIMIT':
            raise definition_exceptions.QuotaAtteint("Changez de clé d'API, la limite a été atteinte avec celle-ci pour aujourd'hui")


        temps_text = result.get('routes')[0].get('legs')[0].get('duration').get('text')


        # Convertir le temps obtenu qui est sous forme de texte en elements utilisables
        temps = temps_text.split(" ")

        # Commençons par les jours
        if "days" in temps:
            day = temps[temps.index("days") -1]
        elif "day" in temps:
            day = temps[temps.index("day") -1]
        else:
            day=0

        # Puis les heures
        if "hours" in temps:
            hour = temps[temps.index("hours") - 1]
        elif "hour" in temps:
            hour = temps[temps.index("hour") - 1]
        else:
            hour = 0

        # Puis les minutes
        if "mins" in temps:
            minute = temps[temps.index("mins") - 1]
        elif "min" in temps:
            minute = temps[temps.index("min") - 1]
        else:
            minute = 0

        time = datetime.timedelta(minutes= int(minute), hours=int(hour), days=int(day))
        return time


    def get_latlong(self,address):
        """Transforme une adresse pour la convertir en coordonnees de geolocalisation"""

        address.replace(" ", "+")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"+&key="+GOOGLE_KEY
        resp = self.communication(url)
        result = resp.json()

        # Si aucun  resultat n'est trouve par Google, il ne renverra pas de resultat, ce qu'il faudra signaler.
        if len(result.get('results')) == 0:
            raise definition_exceptions.AdresseNonComprise("Google ne trouve pas l'adresse")


        coord = result.get('results')[0].get('geometry').get('location')

        # Verifie que les coordonnées du lieu designent bien un lieu dans Paris
        if coord['lng'] < 2.22 or coord['lng'] > 2.44:
            raise  definition_exceptions.AdresseHorsParis("L'adresse '{}' ne semble pas se trouver à Paris".format(address))
        if coord['lat'] < 48.81 or coord['lat'] > 48.91 :
            raise definition_exceptions.AdresseHorsParis("L'adresse '{}' ne semble pas se trouver à Paris".format(address))

        return (coord['lat'], coord['lng'])


class WeatherClass:
    """Definit la classe qui va appeler les services meteo"""
    def __init__(self, city):
        self.city = city

    def does_it_rain(self):
        """Permet de savoir si les conditions meteos sont bonnes"""
        url="http://api.openweathermap.org/data/2.5/weather?q="+self.city+",uk&APPID="+WEATHER_KEY
        try:
            resp = get(url).json()
            meteo = resp.get('weather')[0].get('description')
            weather_call_worked=True
        except:
            weather_call_worked = False

        bad_conditions = ["shower rain", "rain", "thunderstorm", "snow", "mist"]
        if meteo in bad_conditions and weather_call_worked==True:
            return True
        else:
            return False


class OpendataParisClass:
    """Definit les appels a l'OpenData de la ville de Paris pour obtenir des informations sur les Velibs et Autolibs
    Les informations seront traitees dans le fichier des classes Velibs et Autolibs"""

    def call_opendata(self,lat,lng,radius,dataset):
        """Recupere les informations de l'open data en fonction de parametres geographiques"""
        url="https://opendata.paris.fr/api/records/1.0/search/?dataset="+dataset+"&geofilter.distance="+str(lat)+"%2C"+str(lng)+"%2C"+str(radius)
        resp = get(url)
        reponse = resp.json()
        return reponse
