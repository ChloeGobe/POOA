# Webservices projet POOA

from requests import get, HTTPError
from re import sub
import datetime

# Liste des cles d'API necessaires a leur fonctionnement
GOOGLE_KEY = 'AIzaSyCq64SBYC4TlMFNODwtm3D3XXcBsNoNpDw'
WEATHER_KEY = "f3904bf691d361bae156a10d1ab0fc93"
VELIB_KEY= "1a502a8fc4844b5414f7510e95998d40a9f02b4c"

class GoogleClass:
    """Definit les differents services internet de Google qui vont etre necessaires"""

    def __init__(self,departure,arrival,mode):

        # Verifie le type des arguments
        arrival = arrival.encode('utf8')
        departure = departure.encode('utf8')

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
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&destination='+ self.arrival +'&mode=' + self.mode + '&key='+GOOGLE_KEY

        resp = self.communication(url)

        # Permet de verifier qu'une reponse est bien obtenue
        if resp.status_code != 200:
            raise HTTPError('GET /tasks/ {}'.format(resp.status_code))
        result = resp.json()

        # Nettoie les directions de caracteres speciaux
        expression = r'<[^>]*>'
        try:
            directions = [element.get('html_instructions') for element in result.get('routes')[0].get('legs')[0].get('steps')]
            directions_propres = [sub(expression,"",element) for element in directions]
        except:
            directions_propres=["empty"]
        return directions_propres

    def get_time(self):
        """Obtenir le temps de trajet"""

        #Retrieve the get
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&destination='+ self.arrival +'&mode=' + self.mode + '&key='+GOOGLE_KEY
        resp = self.communication(url)

        # Permet de verifier qu'une reponse est bien obtenue
        if resp.status_code != 200:
            raise HTTPError('GET /tasks/ {}'.format(resp.status_code))

        # Transforme le contenu en JSON
        result = resp.json()
        try:
            temps = result.get('routes')[0].get('legs')[0].get('duration').get('text')
        except:
            temps = "7 days"
        # Convertir le temps obtenu qui est sous forme de texte en elements utilisables
        try:
            hour, minute = temps.split("hour")
            minute = minute.split(" ")
            minute = minute[1]
        except:
            hour = 0
            minute = temps.split(" ")
            minute = minute[0]
        time = datetime.timedelta(minutes= int(minute), hours=int(hour))
        return time

    def get_latlong(self,address):
        """Transforme une adresse pour la convertir en coordonnees de geolocalisation"""
        address.replace(" ", "+")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"+&key="+GOOGLE_KEY
        resp = self.communication(url)
        result = resp.json()
        coord = result.get('results')[0].get('geometry').get('location')
        return (coord['lat'], coord['lng'])


class WeatherClass:
    """Definit la classe qui va appeler les services meteo"""
    def __init__(self, city):
        self.city = city

    def does_it_rain(self):
        """Permet de savoir si les conditions meteos sont bonnes"""
        url="http://api.openweathermap.org/data/2.5/weather?q="+self.city+",uk&APPID="+WEATHER_KEY
        resp = get(url).json()
        meteo = resp.get('weather')[0].get('description')
        bad_conditions = ["shower rain", "rain", "thunderstorm", "snow", "mist"]

        if meteo in bad_conditions:
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



if __name__ == '__main__':
    test = GoogleClass("rue de passy","rue saint jacques","TRANSIT")
    etapes = test.get_etapes()
