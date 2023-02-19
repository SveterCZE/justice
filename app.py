#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 09:38:19 2021

@author: sveter
"""
# NEW BUILD BASED ON POSTGRES

import os
import psycopg2
from lxml import etree

def return_conn():
        return psycopg2.connect(
        host="localhost",
        database="justice2023",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# conn = psycopg2.connect(
#         host="localhost",
#         database="justice2023",
#         user=os.environ['DB_USERNAME'],
#         password=os.environ['DB_PASSWORD'])

# cur = conn.cursor()

# app.py
# from flask import Flask
# # from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy
# from config_data import secret_key, db_address
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_address
# app.config["SQLALCHEMY_ECHO"] = False
# app.debug = False
# # HIDE THIS BEFORE DEPLOYING TO PRODUCTION :)
# app.secret_key = secret_key
# # toolbar = DebugToolbarExtension(app)
# db = SQLAlchemy(app)




