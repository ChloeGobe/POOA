# -*- coding: utf-8 -*-

class GoogleClassError(Exception):
    def __init__(self, message):
        self.text = message

class AdresseNonComprise(GoogleClassError):
    pass

class AdresseHorsParis(GoogleClassError):
    pass

class ItineraireNonTrouve(GoogleClassError):
    pass

class QuotaAtteint(GoogleClassError):
    pass

class ModeNonDefini(GoogleClassError):
    pass


class MeteoBroken(Exception):
    def __init__(self,message):
        self.text=message

