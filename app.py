#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NEW BUILD BASED ON POSTGRES

import os
import psycopg2
from lxml import etree
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import JusticeSearchForm
from tables import Results
# from db_config import DB_URI, key
import sqlalchemy as sa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.secret_key = os.environ['DB_KEY']
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

from models import Company, Soudni_Zapisy, \
    Sidlo_Association, Adresy_v2, Pravni_Forma_Association_v2, Pravni_Formy, Nazvy, Insolvency_Events, Konkurz_Events

def return_conn():
        return psycopg2.connect(
        host="localhost",
        database="justice2023",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
        )

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     conn = return_conn()
#     search = JusticeSearchForm(request.form)
#     if request.method == 'POST':
#         return search_results(search)
#     return render_template('search_form.html', form=search)

# @app.route('/results', methods=['GET', 'POST'])
# def search_results(search):
#     results = []

#     ico = search.ico_search.data
#     ico_search_method = search.ico_search_selection.data

#     nazev = search.nazev_subjektu.data
#     nazev_search_method = search.nazev_subjektu_selection.data
#     nazev_actual_or_full = search.nazev_search_actual.data

#     oddil = search.oddil_search.data
#     oddil_search_method = search.oddil_search_selection.data
#     oddil_actual_or_full = search.oddil_search_actual.data

#     vlozka = search.vlozka_search.data
#     vlozka_search_method = search.vlozka_search_selection.data
#     vlozka_actual_or_full = search.vlozka_search_actual.data

#     obec = search.obec_search.data
#     obec_search_method = search.obec_search_selection.data
#     obec_actual_or_full = search.obec_search_actual.data

#     ulice = search.ulice_search.data
#     ulice_search_method = search.ulice_search_selection.data
#     ulice_actual_or_full = search.ulice_search_actual.data

#     co = search.co_search.data
#     co_search_method = search.co_search_selection.data
#     co_actual_or_full = search.co_search_actual.data

#     cp = search.cp_search.data
#     cp_search_method = search.cp_search_selection.data
#     cp_actual_or_full = search.cp_search_actual.data

#     pravni_forma = search.pravni_forma_search.data
#     pravni_forma_actual_or_full = search.pravni_forma_actual.data

#     soud = search.soud_search.data
#     soud_actual_or_full = search.soud_search_actual.data

#     insolvent_only = search.insolvent_only_search.data

#     criminal_record_only = search.criminal_record_only_search.data

#     zapsano_od = search.zapis_od.data
#     zapsano_do = search.zapis_do.data

#     qry = Company.query

#     if insolvent_only:
#         qry = qry.join(Insolvency_Events, Company.insolvence)
#         qry = qry.filter(Insolvency_Events.vymaz_datum == None)
#         qry_konkurz = Company.query
#         qry_konkurz = qry_konkurz.join(Konkurz_Events, Company.konkurz)
#         qry_konkurz = qry_konkurz.filter(Konkurz_Events.vymaz_datum == None)
#         qry = qry.union(qry_konkurz)
#     #
#     # if criminal_record_only:
#     #     qry = qry.join(Criminal_Records, Company.criminal_record)

#     if ico:
#         if ico_search_method == "text_anywhere":
#             qry = qry.filter(Company.ico.contains(ico))
#         elif ico_search_method == "text_beginning":
#             qry = qry.filter(Company.ico.like(f'{ico}%'))
#         elif ico_search_method == "text_exact":
#             qry = qry.filter(Company.ico == ico)

#     if nazev:
#         qry = qry.join(Nazvy, Company.obchodni_firma)
#         if nazev_actual_or_full == "actual_results":
#             qry = qry.filter(Nazvy.vymaz_datum == None)
#         if nazev_search_method == "text_anywhere":
#             qry = qry.filter(sa.func.lower(Nazvy.nazev_text).contains(sa.func.lower(nazev)))
#         elif nazev_search_method == "text_beginning":
#             qry = qry.filter(Nazvy.nazev_text.ilike(f'{nazev}%'))
#         elif nazev_search_method == "text_exact":
#             qry = qry.filter(sa.func.lower(Nazvy.nazev_text) == sa.func.lower(nazev))

#     if oddil:
#         qry = qry.join(Soudni_Zapisy, Company.soudni_zapis)
#         if oddil_actual_or_full == "actual_results":
#             qry = qry.filter(Soudni_Zapisy.vymaz_datum == None)
#         if oddil_search_method == "text_anywhere":
#             qry = qry.filter(Soudni_Zapisy.oddil.contains(oddil))
#         elif oddil_search_method == "text_beginning":
#             qry = qry.filter(Soudni_Zapisy.oddil.like(f'{oddil}%'))
#         elif oddil_search_method == "text_exact":
#             qry = qry.filter(Soudni_Zapisy.oddil == oddil)

#     if vlozka:
#         qry = qry.join(Soudni_Zapisy, Company.soudni_zapis)
#         if vlozka_actual_or_full == "actual_results":
#             qry = qry.filter(Soudni_Zapisy.vymaz_datum == None)
#         if vlozka_search_method == "text_anywhere":
#             qry = qry.filter(Soudni_Zapisy.vlozka.contains(vlozka))
#         elif vlozka_search_method == "text_beginning":
#             qry = qry.filter(Soudni_Zapisy.vlozka.like(f'{vlozka}%'))
#         elif vlozka_search_method == "text_exact":
#             qry = qry.filter(Soudni_Zapisy.vlozka == vlozka)

#     if obec:
#         qry = qry.join(Sidlo_Association, Company.sidlo_text)
#         if obec_actual_or_full == "actual_results":
#             qry = qry.filter(Sidlo_Association.vymaz_datum == None)
#         qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
#         if obec_search_method == "text_anywhere":
#             qry = qry.filter(Adresy_v2.obec.contains(obec))
#         elif obec_search_method == "text_beginning":
#             qry = qry.filter(Adresy_v2.obec.like(f'{obec}%'))
#         elif obec_search_method == "text_exact":
#             qry = qry.filter(Adresy_v2.obec == obec)

#     if ulice:
#         qry = qry.join(Sidlo_Association, Company.sidlo_text)
#         if ulice_actual_or_full == "actual_results":
#             qry = qry.filter(Sidlo_Association.vymaz_datum == None)
#         qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
#         if ulice_search_method == "text_anywhere":
#             qry = qry.filter(Adresy_v2.ulice.contains(ulice))
#         elif ulice_search_method == "text_beginning":
#             qry = qry.filter(Adresy_v2.ulice.like(f'{ulice}%'))
#         elif ulice_search_method == "text_exact":
#             qry = qry.filter(Adresy_v2.ulice == ulice)

#     if cp:
#         qry = qry.join(Sidlo_Association, Company.sidlo_text)
#         if cp_actual_or_full == "actual_results":
#             qry = qry.filter(Sidlo_Association.vymaz_datum == None)
#         qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
#         if cp_search_method == "text_anywhere":
#             qry = qry.filter(Adresy_v2.cislopo.contains(cp))
#         elif cp_search_method == "text_beginning":
#             qry = qry.filter(Adresy_v2.cislopo.like(f'{cp}%'))
#         elif cp_search_method == "text_exact":
#             qry = qry.filter(Adresy_v2.cislopo == cp)

#     if co:
#         qry = qry.join(Sidlo_Association, Company.sidlo_text)
#         if co_actual_or_full == "actual_results":
#             qry = qry.filter(Sidlo_Association.vymaz_datum == None)
#         qry = qry.join(Adresy_v2, Sidlo_Association.sidlo_text)
#         if co_search_method == "text_anywhere":
#             qry = qry.filter(Adresy_v2.cisloor.contains(co))
#         elif co_search_method == "text_beginning":
#             qry = qry.filter(Adresy_v2.cisloor.like(f'{co}%'))
#         elif co_search_method == "text_exact":
#             qry = qry.filter(Adresy_v2.cisloor == co)

#     if pravni_forma:
#         qry = qry.join(Pravni_Forma_Association_v2, Company.pravni_forma_text)
#         if pravni_forma_actual_or_full == "actual_results":
#             qry = qry.filter(Pravni_Forma_Association_v2.vymaz_datum == None)
#         qry = qry.join(Pravni_Formy, Pravni_Forma_Association_v2.pravni_forma_text)
#         qry = qry.filter(Pravni_Formy.pravni_forma == pravni_forma)

#     if soud:
#         qry = qry.join(Soudni_Zapisy, Company.soudni_zapis)
#         if soud_actual_or_full == "actual_results":
#             qry = qry.filter(Soudni_Zapisy.vymaz_datum == None)
#         qry = qry.filter(Soudni_Zapisy.soud == soud)

#     if zapsano_od:
#         qry = qry.filter(Company.zapis >= zapsano_od)
#     if zapsano_do:
#         qry = qry.filter(Company.zapis <= zapsano_do)

#     results = qry.all()

#     if not results:
#         flash('No results found!')
#         return redirect('/')

#     else:
#         table = Results(results)
#         table.border = True
#         return render_template("results2.html", results=results, form=search, zapsano_od=zapsano_od, zapsano_do=zapsano_do, show_form = True)

# conn = psycopg2.connect(
#         host="localhost",
#         database="justice2023",
#         user=os.environ['DB_USERNAME'],
#         password=os.environ['DB_PASSWORD'])

# cur = conn.cursor()

# app.py

# # from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy
# from config_data import secret_key, db_address
#

# app.config['SQLALCHEMY_DATABASE_URI'] = db_address
# app.config["SQLALCHEMY_ECHO"] = False
# app.debug = False
# # HIDE THIS BEFORE DEPLOYING TO PRODUCTION :)
# app.secret_key = secret_key
# # toolbar = DebugToolbarExtension(app)





