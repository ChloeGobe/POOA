# -*- coding: utf-8 -*-

class AdresseNonComprise(Exception):
    pass

class AdresseHorsParis(Exception):
    pass

class ItineraireNonTrouve(Exception):
    pass

class QuotaAtteint(Exception):
    pass

class MeteoBroken(Exception):
    def __init__(self,message):
        self.text=message

class ModeNonDefini(Exception):
    pass
