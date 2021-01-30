#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 11:52:57 2021

@author: sveter
"""

from flask_table import Table, Col

class Results(Table):
    classes = ['table']
    id = Col('Id', show=False)
    nazev = Col('Obchodní firma')
    ico = Col('IČ')
    sidlo = Col('Sídlo')
    zapis = Col('Zápis do OR')
    oddil = Col('Oddíl')
    vlozka = Col('Vložka')
    soud = Col('Rejstříkový soud')