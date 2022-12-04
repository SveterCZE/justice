#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 10:05:34 2021

@author: sveter
"""

from wtforms import Form, StringField, SelectField, BooleanField
from wtforms.fields.html5 import DateField

# CREATE A GENERAL CLASS TO REMOVE DUPLICITIES?

class GeneralSearchForm(Form):
    search_options = [("text_anywhere","Kdekoliv v textu"),
             ("text_beginning","Začátek výrazu"),
             ("text_exact","Přesný výraz"),
             ]
    actual_options = [("actual_results","Jen platné"),
                    ("complete_results","Platné i neplatné"),]

    obec_search = StringField(u'Obec:')
    obec_search_selection = SelectField('', choices=search_options)
    obec_search_actual = SelectField('', choices=actual_options) 
    
    ulice_search = StringField(u'Ulice:')
    ulice_search_selection = SelectField('', choices=search_options)
    ulice_search_actual = SelectField('', choices=actual_options) 

    cp_search = StringField(u'Číslo popisné:')
    cp_search_selection = SelectField('', choices=search_options)
    cp_search_actual = SelectField('', choices=actual_options) 

    co_search = StringField(u'Číslo orientační:')
    co_search_selection = SelectField('', choices=search_options)
    co_search_actual = SelectField('', choices=actual_options) 

class JusticeSearchForm(GeneralSearchForm):   
    search_options = GeneralSearchForm.search_options
    actual_options = GeneralSearchForm.actual_options
    
    nazev_subjektu = StringField(u'Název subjektu:')
    nazev_subjektu_selection = SelectField('', choices=search_options)
    nazev_search_actual = SelectField('', choices=actual_options)

    ico_search = StringField(u'Identifikační číslo:')
    ico_search_selection = SelectField('', choices=search_options) 
       
    oddil_search = StringField(u'Oddíl:')
    oddil_search_selection = SelectField('', choices=search_options) 
    oddil_search_actual = SelectField('', choices=actual_options)
    
    vlozka_search = StringField(u'Vložka:')
    vlozka_search_selection = SelectField('', choices=search_options)
    vlozka_search_actual = SelectField('', choices=actual_options)
    
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
    pravni_forma_actual = SelectField('', choices=actual_options)

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
    soud_search_actual = SelectField('', choices=actual_options)

    insolvent_only_search = BooleanField("Pouze společnosti s insolvenčním zápisem")
    criminal_record_only_search = BooleanField("Pouze společnosti s trestním zápisem")
    
    zapis_do = DateField(u'Zapsáno do:', format='%Y-%m-%d')
    zapis_od = DateField(u'Zapsáno od:', format='%Y-%m-%d')

class PersonSearchForm(GeneralSearchForm):   
    search_options = GeneralSearchForm.search_options
    actual_options = GeneralSearchForm.actual_options

    fist_name_search = StringField(u'Jméno:')
    fist_name_search_selection = SelectField('', choices=search_options)
    fist_name_search_actual = SelectField('', choices=actual_options)

    surname_search = StringField(u'Příjmení:')
    surname_search_selection = SelectField('', choices=search_options)
    surname_search_actual = SelectField('', choices=actual_options)

    person_actual_selection = SelectField('', choices=actual_options)

    birthday = DateField(u'Datum narození:', format='%Y-%m-%d')

class EntitySearchForm(GeneralSearchForm):
    search_options = GeneralSearchForm.search_options
    actual_options = GeneralSearchForm.actual_options

    entity_name_search = StringField(u'Název:')
    entity_name_search_selection = SelectField('', choices=search_options)
    entity_name_search_actual = SelectField('', choices=actual_options)
    
    entity_number_search = StringField(u'IČO nebo zahraniční registrační číslo:')
    entity_number_search_selection = SelectField('', choices=search_options)

    entity_actual_selection = SelectField('', choices=actual_options)                

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


    