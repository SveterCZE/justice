#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 09:38:19 2021

@author: sveter
"""

# app.py
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from key_gen import get_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///justice.db'
app.config["SQLALCHEMY_ECHO"] = True
app.debug = True
app.secret_key = get_key
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)