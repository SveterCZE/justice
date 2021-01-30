#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 09:56:14 2021

@author: sveter
"""

from app import db
from sqlalchemy.orm import relationship, backref

# class Soud(db.Model):
#     __tablename__ = "soudy"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
    
#     def __repr__(self):
#         # return "<soud: {}="">".format(self.name)
#         return self.name

association_table = db.Table("obce_relation",
                                db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
                                db.Column("obec_id", db.Integer, db.ForeignKey("obce.id"), nullable=False),
                                # db.PrimaryKeyConstraint('company_id', 'obec_id')
                                )

ulice_association = db.Table("ulice_relation",
                                db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
                                db.Column("ulice_id", db.Integer, db.ForeignKey("ulice.id"), nullable=False),
                                # db.PrimaryKeyConstraint('company_id', 'obec_id')
                                )

pravni_forma_association=db.Table("pravni_formy_relation",
                                  db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
                                  db.Column("pravni_forma_id", db.Integer, db.ForeignKey("pravni_formy.id"), nullable=False),
                                  )

class Company(db.Model):

    __tablename__ = "companies"   
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String)
    nazev = db.Column(db.String)
    zapis = db.Column(db.String)
    sidlo = db.Column(db.String)
    oddil = db.Column(db.String)
    vlozka = db.Column(db.String)
    soud = db.Column(db.String)
    obec = db.relationship("Obce", secondary=association_table, backref="companies")
    ulice = db.relationship("Ulice", secondary=ulice_association, backref="companies")
    pravni_forma = db.relationship("Pravni_Forma", secondary=pravni_forma_association, backref="companies")
    insolvence = db.relationship("Insolvency_Events", backref="companies")
    

class Obce(db.Model):
    __tablename__ = "obce"
    id = db.Column(db.Integer, primary_key=True)
    obec_jmeno = db.Column(db.String)
    company_obec = db.relationship("Company", secondary=association_table, backref="obce")
    
class Ulice(db.Model):
    __tablename__ = "ulice"
    id = db.Column(db.Integer, primary_key=True)
    ulice_jmeno = db.Column(db.String)
    company_ulice = db.relationship("Company", secondary=ulice_association)    

class Pravni_Forma(db.Model):
    __tablename__ = "pravni_formy"
    id = db.Column(db.Integer, primary_key=True)
    pravni_forma = db.Column(db.String)
    company_pravni_forma = db.relationship("Company", secondary=pravni_forma_association)

class Insolvency_Events(db.Model):
    __tablename__ = "insolvency_events"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    company = relationship("Company", backref="insolvency_events")
    insolvency_event = db.Column(db.String)


# class Association(db.Model):   
#     __tablename__ = "obce_relation"
#     company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
#     obec_id = db.Column(db.Integer, db.ForeignKey('obce.id'))
    
#     company = relationship("Company", back_populates = "Obce")
#     obec = relationship("Obce", back_populates = "Company")
    

        


# </soud:>