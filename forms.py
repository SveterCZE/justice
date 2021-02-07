#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 10:05:34 2021

@author: sveter
"""

from wtforms import Form, StringField, SelectField, BooleanField
from wtforms.fields.html5 import DateField

# class JusticeSearchForm(Form):
#     choices = [('ico', 'Identifikační číslo'),
#                ('nazev', 'Obchodní firma'),]
#     select = SelectField('Search for company:', choices=choices)
#     search = StringField('')

class JusticeSearchForm(Form):
    search_options = [("text_anywhere","Kedkoliv v textu"),
             ("text_beginning","Začátek výrazu"),
             ("text_exact","Přesný výraz"),
             ]
    nazev_subjektu = StringField(u'Název subjektu:')
    nazev_subjektu_selection = SelectField('', choices=search_options)
    ico_search = StringField(u'Identifikační číslo:')
    ico_search_selection = SelectField('', choices=search_options) 
    obec_search = StringField(u'Obec:')
    obec_search_selection = SelectField('', choices=search_options) 
    ulice_search = StringField(u'Ulice:')
    ulice_search_selection = SelectField('', choices=search_options) 
    oddil_search = StringField(u'Oddíl:')
    oddil_search_selection = SelectField('', choices=search_options) 
    vlozka_search = StringField(u'Vložka:')
    vlozka_search_selection = SelectField('', choices=search_options) 
    formy = [       ("",""),
                    ('Akciová společnost', 'Akciová společnost'),
                   ('Společnost s ručením omezeným', 'Společnost s ručením omezeným'),
                   ('Veřejná obchodní společnost', 'Veřejná obchodní společnost'),
                   ('Komanditní společnost', 'Komanditní společnost'),
                   ('Družstvo', 'Družstvo'),
                   ('Zájmové sdružení právnických osob', 'Zájmové sdružení právnických osob'),
                   ('Zahraniční fyzická osoba ', 'Zahraniční fyzická osoba '),
                   ('Ústav', 'Ústav'),
                   ('Společenství vlastníků jednotek', 'Společenství vlastníků jednotek'),
                   ('Spolek', 'Spolek'),
                   ('Příspěvková organizace', 'Příspěvková organizace'),
                   ('Pobočný spolek', 'Pobočný spolek'),
                   ('Odštěpný závod zahraniční právnické osoby', 'Odštěpný závod zahraniční právnické osoby'),
                   ('Organizační složka zahraničního nadačního fondu', 'Organizační složka zahraničního nadačního fondu'),
                   ('Organizační složka zahraniční nadace', 'Organizační složka zahraniční nadace'),
                   ('Organizace zaměstnavatelů', 'Organizace zaměstnavatelů'),
                   ('Odborová organizace', 'Odborová organizace'),
                   ('Nadační fond', 'Nadační fond'),
                   ('Nadace', 'Nadace'),
                   ('Evropská společnost', 'Evropská společnost'),
                   ('Evropské hospodářské zájmové sdružení', 'Evropské hospodářské zájmové sdružení'),
                   ('Evropská družstevní společnost', 'Evropská družstevní společnost'),
                   ]
    pravni_forma_search = SelectField(u'Právní forma:', choices=formy)
    soudy = [("",""),
             ("MSPH","Městský soud v Praze"),
             ("KSCB","Krajský soud v Českých Budějovicích"),
             ("KSPL","Krajský soud v Plzni"),
             ("KSUL","Krajský soud v Ústí nad Labem"),
             ("KSHK","Krajský soud v Hradci Králové"),
             ("KSBR","Krajský soud v Brně"),
             ("KSOS","Krajský soud v Ostravě"),
             ] 
    soud_search = SelectField(u'Rejstříkjový soud:', choices=soudy)   
    insolvent_only_search = BooleanField("Pouze společnosti s insolvenčním zápisem")
    zapis_do = DateField(u'Zapsáno do:', format='%Y-%m-%d')
    zapis_od = DateField(u'Zapsáno od:', format='%Y-%m-%d')
    
    

    
class CompanyForm(Form):
    oddil = [('A', 'A'),
                   ('B', 'B'),
                   ('C', 'C'),
                   ]
    ico = StringField('ico')
    nazev = StringField('nazev')
    zapis = StringField('zapis')
    sidlo = StringField('sidlo')
    oddil = SelectField('oddil', choices=oddil)
    vlozka = StringField('vlozka')
    soud = StringField('soud')
    
    