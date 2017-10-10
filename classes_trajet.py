##Classe qui definir les differents trajets
import webservices

class Trajet:
    """Definit la classe trajet generale, notamment les trajets a pied"""
    def __init__(self, lieu_depart, lieu_arrivee):
        self.lieu_depart = lieu_depart
        self.lieu_arrivee = lieu_arrivee
        self.etape_iti = []
        self.temps_trajet = 0

    def get_temps_pied (self):
        """Fait appel au service web Google Maps pour les trajets a pied"""
        web_services_google = webservices.GoogleClass(self.lieu_depart, self.lieu_arrivee, "WALKING")
        temps = web_services_google.get_time()
        return temps
