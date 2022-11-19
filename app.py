#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 09:38:19 2021

@author: sveter
"""

# app.py
from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from config_data import secret_key, db_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_address
app.config["SQLALCHEMY_ECHO"] = False
app.debug = False
# HIDE THIS BEFORE DEPLOYING TO PRODUCTION :)
app.secret_key = secret_key
# toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)