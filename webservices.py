# Webservices projet POOA

from requests import get, HTTPError
from re import sub
import datetime

GOOGLE_KEY = 'AIzaSyCq64SBYC4TlMFNODwtm3D3XXcBsNoNpDw'
WEATHER_KEY = "f3904bf691d361bae156a10d1ab0fc93"
VELIB_KEY= "1a502a8fc4844b5414f7510e95998d40a9f02b4c"

class GoogleClass:
        def __init__(self,departure,arrival,mode):

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
            resp = get(url)
            return resp

        def get_etapes(self):
            url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&destination='+ self.arrival +'&mode=' + self.mode + '&key='+GOOGLE_KEY
            resp = self.communication(url)
            if resp.status_code != 200:
                raise HTTPError('GET /tasks/ {}'.format(resp.status_code))
            result = resp.json()
            #Retrieve the directions from the result
            #Clean the directions from html using a regex
            expression = r'<[^>]*>'
            directions = [element.get('html_instructions') for element in result.get('routes')[0].get('legs')[0].get('steps')]
            directions_propres = [sub(expression,"",element) for element in directions]
            return directions_propres

        def get_time(self):
            #Retrieve the get
            url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&destination='+ self.arrival +'&mode=' + self.mode + '&key='+GOOGLE_KEY
            resp = self.communication(url)
            if resp.status_code != 200:
                # This means something went wrong.
                raise HTTPError('GET /tasks/ {}'.format(resp.status_code))
            #Parse the Get response into a JSON
            result = resp.json()
            #Retrieve the directions from the result
            temps = result.get('routes')[0].get('legs')[0].get('duration').get('text')

            try:
                hour, minute = temps.split("hour")
                minute = minute.split(" ")
                minute = minute[1]
            except:
                hour = 0
                minute = temps.split(" ")
                minute = minute[0]
            time = datetime.time(hour, minute)
            return time

        def get_latlong(self,address):
            # We shall start by a transformation of the adress into something we can send to google
            address.replace(" ", "+")
            url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"+&key="+GOOGLE_KEY
            resp = self.communication(url)
            result = resp.json()
            coord = result['results'][0]['geometry']['location']
            return (coord['lat'], coord['lng'])


class WeatherClass:
    def get_ifit_rains(self,city):
        url="http://api.openweathermap.org/data/2.5/weather?q="+city+",uk&APPID="+WEATHER_KEY
        resp = get(url)
        return resp.json()


class OpendataParisClass:
    def call_opendata(self,lat,lng,radius,dataset):
        url="https://opendata.paris.fr/api/records/1.0/search/?dataset="+dataset+"&facet=ville&facet=cp&facet=type&sort=dist&geofilter.distance="+str(lat)+"%2C"+str(lng)+"%2C"+str(radius)
        resp = get(url)
        reponse = resp.json()
        return reponse

