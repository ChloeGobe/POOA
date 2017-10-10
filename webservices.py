# Webservices projet POOA

from requests import get, HTTPError
from re import sub

GOOGLE_KEY = 'AIzaSyCq64SBYC4TlMFNODwtm3D3XXcBsNoNpDw'

class GoogleClass(depart, arrivee, mode):


        def __init__(self,departure,arrival,mode):

            if not isinstance(departure, str):
                raise TypeError("Le departure doit être une chaîne de caractères")
            if not isinstance(arrival, str):
                raise TypeError("Le arrival doit être une chaîne de caractères")
            if not isinstance(mode, str):
                raise TypeError("Le nom doit être une chaîne de caractères")

            self.departure = departure
            self.arrival = arrival
            self.duration = duration
            self.mode=mode

        def communication (self,url):
            resp = get(url)
            return resp


        def get_temps(self):

            #Retrieve the get
            url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+ self.departure + '&destination='+ self.arrival +'&mode=' + self.mode + '&key='+GOOGLE_KEY')
            resp = self.communication(url)

            if resp.status_code != 200:
                # This means something went wrong.
                raise HTTPError('GET /tasks/ {}'.format(resp.status_code))

            #Parse the Get response into a JSON
            result = resp.json()
            #Retrieve the directions from the result
            temps = [element.get('html_instructions') for element in result.get('routes')[0].get('legs')[0].get('duration').get('text')]
            #Clean the directions from html using a regex
            #expression = r'<[^>]*>'
            #directions_propres = [sub(expression,"",element) for element in directions]

            #Print directions
            self.duration = temps
