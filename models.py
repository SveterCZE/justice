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

def convert_soud_to_string(my_soud):
    if my_soud == "MSPH":
        return "Městského soudu v Praze"
    elif my_soud == "KSCB":
        return "Krajského soudu v Českých Budějovicích"
    elif my_soud == "KSPL":
        return "Krajského soudu v Plzni"
    elif my_soud == "KSUL":
        return "Krajského soudu v Ústí nad Labem"
    elif my_soud == "KSHK":
        return "Krajského soudu v Hradci Králové"
    elif my_soud == "KSBR":
        return "Krajského soudu v Brně"
    elif my_soud == "KSOS":
        return "Krajského soudu v Ostravě"
    else:
        return "podivného soudu"

class MyType(types.TypeDecorator):

    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        return convert_date_to_string(value)

    def process_result_value(self, value, dialect):
        # return "PREFIX:" + value
        return convert_date_to_string(value)

    def copy(self, **kw):
        return MyType(self.impl.length)

class MySoud(types.TypeDecorator):

    impl = types.Unicode

    # def process_bind_param(self, value, dialect):
    #     return convert_soud_to_string(value)

    def process_result_value(self, value, dialect):
        # return "PREFIX:" + value
        return convert_soud_to_string(value)

    def copy(self, **kw):
        return MySoud(self.impl.length)


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

# pravni_forma_association=db.Table("pravni_formy_relation",
#                                   db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
#                                   db.Column("pravni_forma_id", db.Integer, db.ForeignKey("pravni_formy.id"), nullable=False),
#                                   )

# predmety_podnikani_association = db.Table("predmety_podnikani_relation",
#                                 db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
#                                 db.Column("predmet_podnikani_id", db.Integer, db.ForeignKey("predmety_podnikani.id"), nullable=False),
#                                 db.Column("zapis_datum", db.String),
#                                 db.Column("vymaz_datum", db.String),
#                                 )


class Predmety_Podnikani_Association(db.Model):
    __tablename__ = 'predmety_podnikani_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    predmet_podnikani_id = db.Column(db.Integer, db.ForeignKey('predmety_podnikani.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_podnikani = db.relationship("Predmet_Podnikani", back_populates="company_predmet_podnikani")
    company = db.relationship("Company", back_populates="predmet_podnikani")

class Predmety_Cinnosti_Association(db.Model):
    __tablename__ = 'predmety_cinnosti_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    predmet_cinnosti_id = db.Column(db.Integer, db.ForeignKey('predmety_cinnosti.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_cinnosti = db.relationship("Predmet_Cinnosti", back_populates="company_predmet_cinnosti")
    company = db.relationship("Company", back_populates="predmet_cinnosti")

class Sidlo_Association(db.Model):
    __tablename__ = 'sidlo_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    sidlo_id = db.Column(db.Integer, db.ForeignKey('adresy.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    sidlo_text = db.relationship("Sidlo", back_populates="company_sidlo")
    company = db.relationship("Company", back_populates="sidlo_text")

class Pravni_Forma_Association_v2(db.Model):
    __tablename__ = 'pravni_formy_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    pravni_forma_id = db.Column(db.Integer, db.ForeignKey('pravni_formy.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    pravni_forma_text = db.relationship("Pravni_Formy", back_populates="company_pravni_forma")
    company = db.relationship("Company", back_populates="pravni_forma_text")



class Statutarni_Organ_Association(db.Model):
    __tablename__ = 'statutarni_organ_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organy.id'), nullable=False, primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    statutarni_organ_text = db.relationship("Statutarni_Organy", back_populates="company_statutarni_organ")
    company = db.relationship("Company", back_populates="statutarni_organ_text")
    pocet_clenu = db.relationship("Pocty_Clenu_Organu", backref="statutarni_organ_relation")
    zpusoby_jednani = db.relationship("Zpusob_Jednani_Association", back_populates="statutarni_organ")


class Zpusob_Jednani_Association(db.Model):
    __tablename__ = 'zpusoby_jednani_relation'
    id = db.Column(db.Integer, primary_key=True)
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organ_relation.id'), nullable=False)
    zpusob_jednani_id = db.Column(db.Integer, db.ForeignKey('zpusoby_jednani.id'), nullable=False)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    zpusob_jednani = relationship("Zpusob_Jednani", back_populates="zpusob_jednani_rship")
    statutarni_organ = relationship("Statutarni_Organ_Association", back_populates="zpusoby_jednani")      


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
    # pravni_forma = db.relationship("Pravni_Forma", secondary=pravni_forma_association, backref="companies")
    insolvence = db.relationship("Insolvency_Events", backref="companies")
    konkurz = db.relationship("Konkurz_Events", backref="companies")
    predmet_podnikani = db.relationship("Predmety_Podnikani_Association", back_populates="company")
    predmet_cinnosti = db.relationship("Predmety_Cinnosti_Association", back_populates="company")
    zakladni_kapital =  db.relationship("Zakladni_Kapital", backref="companies")
    ostatni_skutecnosti = db.relationship("Ostatni_Skutecnosti", backref="companies")
    akcie = db.relationship("Akcie", backref="companies")
    obchodni_firma = db.relationship("Nazvy", backref="companies")
    soudni_zapis = db.relationship("Soudni_Zapisy", backref="companies")
    sidlo_text = db.relationship("Sidlo_Association", back_populates="company")
    pravni_forma_text = db.relationship("Pravni_Forma_Association_v2", back_populates="company")
    statutarni_organ_text = db.relationship("Statutarni_Organ_Association", back_populates="company")


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

# class Pravni_Forma(db.Model):
#     __tablename__ = "pravni_formy"
#     id = db.Column(db.Integer, primary_key=True)
#     pravni_forma = db.Column(db.String)
#     company_pravni_forma = db.relationship("Company", secondary=pravni_forma_association)

class Insolvency_Events(db.Model):
    __tablename__ = "insolvency_events"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    # company = db.relationship("Company", backref="insolvency_events")
    insolvency_event = db.Column(db.String)

class Konkurz_Events(db.Model):
    __tablename__ = "konkurz_events"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    # company = db.relationship("Company", backref="insolvency_events")
    konkurz_event = db.Column(db.String)

class Zakladni_Kapital(db.Model):
    __tablename__ = "zakladni_kapital"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    vklad_typ = db.Column(db.String)
    vklad_hodnota = db.Column(db.String)
    splaceni_typ = db.Column(db.String)
    splaceni_hodnota = db.Column(db.String)

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

class Sidlo(db.Model):
    __tablename__ = "adresy"
    id = db.Column(db.Integer, primary_key=True)
    adresa_text = db.Column(db.String)
    company_sidlo = db.relationship("Sidlo_Association", back_populates="sidlo_text")

class Pravni_Formy(db.Model):
    __tablename__ = "pravni_formy"
    id = db.Column(db.Integer, primary_key=True)
    pravni_forma = db.Column(db.String)
    company_pravni_forma = db.relationship("Pravni_Forma_Association_v2", back_populates="pravni_forma_text")

class Statutarni_Organy(db.Model):
    __tablename__ = "statutarni_organy"
    id = db.Column(db.Integer, primary_key=True)
    statutarni_organ_text = db.Column(db.String)
    company_statutarni_organ = db.relationship("Statutarni_Organ_Association", back_populates="statutarni_organ_text")

class Ostatni_Skutecnosti(db.Model):
    __tablename__ = "ostatni_skutecnosti"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    ostatni_skutecnost = db.Column(db.String)

class Akcie(db.Model):
    __tablename__ = "akcie"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    akcie_podoba = db.Column(db.String)
    akcie_typ = db.Column(db.String)
    akcie_pocet = db.Column(db.String)
    akcie_hodnota_typ = db.Column(db.String)
    akcie_hodnota_value = db.Column(db.String)
    akcie_text = db.Column(db.String)

class Nazvy(db.Model):
    __tablename__ = "nazvy"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    nazev_text = db.Column(db.String)

class Soudni_Zapisy(db.Model):
    __tablename__ = "zapis_soudy"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    oddil = db.Column(db.String)
    vlozka = db.Column(db.String)
    soud = db.Column(MySoud)

class Pocty_Clenu_Organu(db.Model):
    __tablename__ = "pocty_clenu_organu"
    id = db.Column(db.Integer, primary_key=True)
    organ_id = db.Column(db.String, db.ForeignKey("statutarni_organ_relation.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    pocet_clenu_value = db.Column(db.String)

class Zpusob_Jednani(db.Model):
    __tablename__ = "zpusoby_jednani"
    id = db.Column(db.Integer, primary_key=True)
    zpusob_jednani_text = db.Column(db.String)
    zpusob_jednani_rship = db.relationship("Zpusob_Jednani_Association", back_populates="zpusob_jednani")