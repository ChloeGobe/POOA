# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Iti(models.Model):
    depart = models.CharField(max_length=200)
    arrivee = models.CharField(max_length=200)
