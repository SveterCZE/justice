#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 09:56:14 2021

@author: sveter
"""

from app import db
from sqlalchemy.orm import relationship, backref
import sqlalchemy.types as types


def convert_date_to_string(converted_date):
    if converted_date == 0:
        return converted_date
    else:
        separated_string = converted_date.split("-")
        converted_string = "".join([strip_zero_from_date(separated_string[2]), ". ", convert_month_to_string(separated_string[1]), " ", separated_string[0]])
    return converted_string

def strip_zero_from_date(converted_date):
    if converted_date[0] == "0":
        return converted_date[1]
    else:
        return converted_date

def convert_month_to_string(my_month):
    if my_month == "01":
        return "ledna"
    elif my_month == "02":
        return "února"
    elif my_month == "03":
        return "března"
    elif my_month == "04":
        return "dubna"
    elif my_month == "05":
        return "května"
    elif my_month == "06":
        return "června"
    elif my_month == "07":
        return "července"
    elif my_month == "08":
        return "srpna"
    elif my_month == "09":
        return "září"
    elif my_month == "10":
        return "října"
    elif my_month == "11":
        return "listopadu"
    elif my_month == "12":
        return "prosince"
    else:
        return "podivného měsíce"

class MyType(types.TypeDecorator):
    '''Prefixes Unicode values with "PREFIX:" on the way in and
    strips it off on the way out.
    '''

    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        return convert_date_to_string(value)

    def process_result_value(self, value, dialect):
        # return "PREFIX:" + value
        return convert_date_to_string(value)

    def copy(self, **kw):
        return MyType(self.impl.length)


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

# predmety_podnikani_association = db.Table("predmety_podnikani_relation",
#                                 db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
#                                 db.Column("predmet_podnikani_id", db.Integer, db.ForeignKey("predmety_podnikani.id"), nullable=False),
#                                 db.Column("zapis_datum", db.String),
#                                 db.Column("vymaz_datum", db.String),
#                                 )


class Predmety_Podnikani_Association(db.Model):
    __tablename__ = 'predmety_podnikani_relation'
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    predmet_podnikani_id = db.Column(db.Integer, db.ForeignKey('predmety_podnikani.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_podnikani = db.relationship("Predmet_Podnikani", back_populates="company_predmet_podnikani")
    company = db.relationship("Company", back_populates="predmet_podnikani")

class Predmety_Cinnosti_Association(db.Model):
    __tablename__ = 'predmety_cinnosti_relation'
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    predmet_cinnosti_id = db.Column(db.Integer, db.ForeignKey('predmety_cinnosti.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_cinnosti = db.relationship("Predmet_Cinnosti", back_populates="company_predmet_cinnosti")
    company = db.relationship("Company", back_populates="predmet_cinnosti")


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
    predmet_podnikani = db.relationship("Predmety_Podnikani_Association", back_populates="company")
    predmet_cinnosti = db.relationship("Predmety_Cinnosti_Association", back_populates="company")
    

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
    company = db.relationship("Company", backref="insolvency_events")
    insolvency_event = db.Column(db.String)

class Predmet_Podnikani(db.Model):
    __tablename__ = "predmety_podnikani"
    id = db.Column(db.Integer, primary_key=True)
    predmet_podnikani = db.Column(db.String)
    company_predmet_podnikani = db.relationship("Predmety_Podnikani_Association", back_populates="predmet_podnikani")

class Predmet_Cinnosti(db.Model):
    __tablename__ = "predmety_cinnosti"
    id = db.Column(db.Integer, primary_key=True)
    predmet_cinnosti = db.Column(db.String)
    company_predmet_cinnosti = db.relationship("Predmety_Cinnosti_Association", back_populates="predmet_cinnosti")
