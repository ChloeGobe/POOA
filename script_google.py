# Call API Google Maps
# Input: lieu ou on veut aller, lieu ou l'on est
# Output: Json avec itineraire

from requests import get, HTTPError
from re import sub

def google_api_search(depart, arrivee):

    print("")

    #Retrieve the get
    resp = get('https://maps.googleapis.com/maps/api/directions/json?origin='+ depart + '&destination='+ arrivee +'&mode=DRIVING&key=AIzaSyCq64SBYC4TlMFNODwtm3D3XXcBsNoNpDw')
    if resp.status_code != 200:

        # This means something went wrong.
        raise HTTPError('GET /tasks/ {}'.format(resp.status_code))

    #Parse the Get response into a JSON
    result = resp.json()

    #Retrieve the directions from the result
    directions = [element.get('html_instructions') for element in result.get('routes')[0].get('legs')[0].get('steps')]

    #Clean the directions from html using a regex
    expression = r'<[^>]*>'

    directions_propres = [sub(expression,"",element) for element in directions]

    #Print directions
    for instructions in directions_propres:
        print("{} - {}".format(directions_propres.index(instructions),instructions))