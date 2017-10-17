# Webservices projet POOA

from requests import get, HTTPError
from re import sub
import datetime
from veliberator.geofinder import BaseGeoFinder

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
            time = 60 * int(hour) + int(minute)
            return time

class WeatherClass:
    def get_ifit_rains(self,city):
        url="http://api.openweathermap.org/data/2.5/weather?q="+city+",uk&APPID="+WEATHER_KEY
        resp = get(url)
        return resp

class VelibClass:
    def get_stations_list(self):
        url=" https://api.jcdecaux.com/vls/v1/stations?contract=Paris&apiKey="+VELIB_KEY
        resp = get(url)
        return resp

    def get_closest_station(self,lat,longi):
        geo = BaseGeoFinder(lat,longi)
        stations_around = get.get_stations_around(3)
        print(stations_around)

        return(stations_around)
