#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db
from sqlalchemy.orm import relationship, backref
import sqlalchemy.types as types


def convert_date_to_string(converted_date):
    try:
        if converted_date == 0:
            return converted_date
        else:
            separated_string = converted_date.split("-")
            converted_string = "".join([strip_zero_from_date(separated_string[2]), ". ", convert_month_to_string(separated_string[1]), " ", separated_string[0]])
        return converted_string
    except:
        return ""

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

    def process_result_value(self, value, dialect):
        return convert_date_to_string(value)

    def copy(self, **kw):
        return MyType(self.impl.length)

class MySoud(types.TypeDecorator):

    impl = types.Unicode

    def process_result_value(self, value, dialect):
        return convert_soud_to_string(value)

    def copy(self, **kw):
        return MySoud(self.impl.length)


# association_table = db.Table("obce_relation",
#                                 db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
#                                 db.Column("obec_id", db.Integer, db.ForeignKey("obce.id"), nullable=False),
#                                 )

# ulice_association = db.Table("ulice_relation",
#                                 db.Column("company_id", db.Integer, db.ForeignKey("companies.id"), primary_key=True, nullable=False),
#                                 db.Column("ulice_id", db.Integer, db.ForeignKey("ulice.id"), nullable=False),
#                                 )

class Predmety_Podnikani_Association(db.Model):
    __tablename__ = 'predmety_podnikani_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    predmet_podnikani_id = db.Column(db.Integer, db.ForeignKey('predmety_podnikani.id'), primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_podnikani = db.relationship("Predmet_Podnikani", back_populates="company_predmet_podnikani")
    company = db.relationship("Company", back_populates="predmet_podnikani")

class Predmety_Cinnosti_Association(db.Model):
    __tablename__ = 'predmety_cinnosti_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    predmet_cinnosti_id = db.Column(db.Integer, db.ForeignKey('predmety_cinnosti.id'), primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_cinnosti = db.relationship("Predmet_Cinnosti")
    company = db.relationship("Company")

class Sidlo_Association(db.Model):
    __tablename__ = 'sidlo_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    sidlo_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    sidlo_text = db.relationship("Adresy_v2")
    company = db.relationship("Company")

class Pravni_Forma_Association_v2(db.Model):
    __tablename__ = 'pravni_formy_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    pravni_forma_id = db.Column(db.Integer, db.ForeignKey('pravni_formy.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    pravni_forma_text = db.relationship("Pravni_Formy")
    company = db.relationship("Company")

class Statutarni_Organ_Association(db.Model):
    __tablename__ = 'statutarni_organ_relation'
    id = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organy.id'), primary_key=True)
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    statutarni_organ_text = db.relationship("Statutarni_Organy")
    company = db.relationship("Company")
    pocet_clenu = db.relationship("Pocty_Clenu_Organu")
    zpusoby_jednani = db.relationship("Zpusob_Jednani_Association")
    clenove = db.relationship("Statutarni_Organ_Clen_Association")

class Dozorci_Rada_Association(db.Model):
    __tablename__ = 'dozorci_rada_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    pocet_clenu = db.relationship("Pocty_Clenu_DR")
    clenove = db.relationship("Dozorci_Rada_Clen_Association")

class Statutarni_Organ_Clen_Association(db.Model):
    __tablename__ = 'statutarni_organ_clen_relation'
    id = db.Column(db.Integer, primary_key=True)
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organ_relation.id'))
    osoba_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    funkce_od = db.Column(MyType)
    funkce_do = db.Column(MyType)
    clenstvi_od = db.Column(MyType)
    clenstvi_do = db.Column(MyType)
    funkce = db.Column(db.String)
    adresa = db.relationship("Adresy_v2")
    jmeno = db.relationship("Fyzicka_Osoba")

class Dozorci_Rada_Clen_Association(db.Model):
    __tablename__ = 'dr_organ_clen_relation'
    id = db.Column(db.Integer, primary_key=True)
    dozorci_rada_id = db.Column(db.Integer, db.ForeignKey('dozorci_rada_relation.id'))
    osoba_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    funkce_od = db.Column(MyType)
    funkce_do = db.Column(MyType)
    clenstvi_od = db.Column(MyType)
    clenstvi_do = db.Column(MyType)
    funkce = db.Column(db.String)
    adresa = db.relationship("Adresy_v2")
    jmeno = db.relationship("Fyzicka_Osoba")

class Spolecnici_Association(db.Model):
    __tablename__ = "spolecnici"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    spolecnik_fo_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    spolecnik_po_id = db.Column(db.Integer, db.ForeignKey('pravnicke_osoby.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    text_spolecnik = db.Column(db.String)
    adresa = db.relationship("Adresy_v2")
    jmeno = db.relationship("Fyzicka_Osoba")
    oznaceni_po = db.relationship("Pravnicka_Osoba")
    podily = db.relationship("Podily_Association")

class Prokurista_Association(db.Model):
    __tablename__ = "prokuriste"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    prokurista_fo_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    adresa = db.relationship("Adresy_v2")
    jmeno = db.relationship("Fyzicka_Osoba")
    text_prokurista = db.Column(db.String)

class Prokura_Common_Text_Association(db.Model):
    __tablename__ = "prokura_common_texts"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    prokura_text = db.Column(db.String)    

class Jediny_Akcionar_Association(db.Model):
    __tablename__ = "jediny_akcionar"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    text_akcionar = db.Column(db.String)
    akcionar_fo_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    akcionar_po_id = db.Column(db.Integer, db.ForeignKey('pravnicke_osoby.id'))
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    adresa = db.relationship("Adresy_v2")
    jmeno = db.relationship("Fyzicka_Osoba")
    oznaceni_po = db.relationship("Pravnicka_Osoba")

class Podily_Association(db.Model):
    __tablename__ = "podily"
    id = db.Column(db.Integer, primary_key=True)
    spolecnik_id = db.Column(db.Integer, db.ForeignKey('spolecnici.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    druh_podilu_id = db.Column(db.Integer, db.ForeignKey('druhy_podilu.id'))
    vklad_typ = db.Column(db.String)
    vklad_text = db.Column(db.String)
    souhrn_typ = db.Column(db.String)
    souhrn_text = db.Column(db.String)
    splaceni_typ = db.Column(db.String)
    splaceni_text = db.Column(db.String)
    druh_podilu = db.relationship("Druhy_Podilu")

class Zpusob_Jednani_Association(db.Model):
    __tablename__ = 'zpusoby_jednani_relation'
    id = db.Column(db.Integer, primary_key=True)
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organ_relation.id'))
    zpusob_jednani_id = db.Column(db.Integer, db.ForeignKey('zpusoby_jednani.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    zpusob_jednani = relationship("Zpusob_Jednani")
    statutarni_organ = relationship("Statutarni_Organ_Association")      

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String)
    nazev = db.Column(db.String)
    zapis = db.Column(MyType)
    oddil = db.Column(db.String)
    vlozka = db.Column(db.String)
    soud = db.Column(MySoud)
    insolvence = db.relationship("Insolvency_Events")
    konkurz = db.relationship("Konkurz_Events")
    predmet_podnikani = db.relationship("Predmety_Podnikani_Association")
    predmet_cinnosti = db.relationship("Predmety_Cinnosti_Association")
    zakladni_kapital =  db.relationship("Zakladni_Kapital")
    ostatni_skutecnosti = db.relationship("Ostatni_Skutecnosti")
    akcie = db.relationship("Akcie")
    obchodni_firma = db.relationship("Nazvy")
    soudni_zapis = db.relationship("Soudni_Zapisy")
    pravni_forma_text = db.relationship("Pravni_Forma_Association_v2")
    statutarni_organ_text = db.relationship("Statutarni_Organ_Association")
    dozorci_rada_text = db.relationship("Dozorci_Rada_Association")
    spolecnici = db.relationship("Spolecnici_Association")
    prokurista = db.relationship("Prokurista_Association")
    prokura_common_text = db.relationship("Prokura_Common_Text_Association")
    jediny_akcionar = db.relationship("Jediny_Akcionar_Association")
    sidlo_text = db.relationship("Sidlo_Association")

class Adresy_v2(db.Model):
    __tablename__ = "adresy_v2"
    id = db.Column(db.Integer, primary_key=True)
    stat = db.Column(db.String)
    obec = db.Column(db.String)
    ulice = db.Column(db.String)
    castObce = db.Column(db.String)
    cisloPo = db.Column(db.Integer)
    cisloOr = db.Column(db.Integer)
    psc = db.Column(db.String)
    okres = db.Column(db.String)
    komplet_adresa = db.Column(db.String)
    cisloEv = db.Column(db.Integer)
    cisloText = db.Column(db.String)
    company_sidlo = db.relationship("Sidlo_Association")

    def __repr__(self):
        joined_address = ""
        if self.komplet_adresa != "0":
            return self.komplet_adresa
        if self.ulice != "0":
            joined_address += self.ulice + " "
        if self.cisloText != "0":
            joined_address += self.cisloText + ", "   
        if self.cisloPo != 0:
            if self.ulice == "0":
                joined_address += "č.p. "
            joined_address += str(self.cisloPo)
            if self.cisloOr != 0:
                joined_address += "/"
            else:
                joined_address += ", "
        if self.cisloOr != 0:
            joined_address += str(self.cisloOr) + ", "
        if self.cisloEv != 0:
            joined_address += str(self.cisloEv) + ", "
        if (self.castObce != "0") and (self.castObce != self.obec):
            joined_address += self.castObce + ", "
        if self.psc != "0" and self.psc != None:
            joined_address += self.psc + " "
        if self.obec != "0":
            joined_address += self.obec
        if (self.stat != "Česká republika") and (self.stat != "Česká republika - neztotožněno"):
            joined_address += ", " + self.stat
        return joined_address

# class Obce(db.Model):
#     __tablename__ = "obce"
#     id = db.Column(db.Integer, primary_key=True)
#     obec_jmeno = db.Column(db.String)
#     company_obec = db.relationship("Company", secondary=association_table, backref="obce")

# class Ulice(db.Model):
#     __tablename__ = "ulice"
#     id = db.Column(db.Integer, primary_key=True)
#     ulice_jmeno = db.Column(db.String)
#     company_ulice = db.relationship("Company", secondary=ulice_association)

class Insolvency_Events(db.Model):
    __tablename__ = "insolvency_events"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    insolvency_event = db.Column(db.String)

class Konkurz_Events(db.Model):
    __tablename__ = "konkurz_events"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
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
    company_predmet_podnikani = db.relationship("Predmety_Podnikani_Association")

class Predmet_Cinnosti(db.Model):
    __tablename__ = "predmety_cinnosti"
    id = db.Column(db.Integer, primary_key=True)
    predmet_cinnosti = db.Column(db.String)
    company_predmet_cinnosti = db.relationship("Predmety_Cinnosti_Association")

class Sidlo(db.Model):
    __tablename__ = "adresy"
    id = db.Column(db.Integer, primary_key=True)
    adresa_text = db.Column(db.String)

class Pravni_Formy(db.Model):
    __tablename__ = "pravni_formy"
    id = db.Column(db.Integer, primary_key=True)
    pravni_forma = db.Column(db.String)
    company_pravni_forma = db.relationship("Pravni_Forma_Association_v2")

class Statutarni_Organy(db.Model):
    __tablename__ = "statutarni_organy"
    id = db.Column(db.Integer, primary_key=True)
    statutarni_organ_text = db.Column(db.String)
    company_statutarni_organ = db.relationship("Statutarni_Organ_Association")

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

class Pocty_Clenu_DR(db.Model):
    __tablename__ = "pocty_clenu_DR"
    id = db.Column(db.Integer, primary_key=True)
    organ_id = db.Column(db.String, db.ForeignKey("dozorci_rada_relation.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    pocet_clenu_value = db.Column(db.String)

class Zpusob_Jednani(db.Model):
    __tablename__ = "zpusoby_jednani"
    id = db.Column(db.Integer, primary_key=True)
    zpusob_jednani_text = db.Column(db.String)
    zpusob_jednani_rship = db.relationship("Zpusob_Jednani_Association")

class Druhy_Podilu(db.Model):
    __tablename__ = "druhy_podilu"
    id = db.Column(db.Integer, primary_key=True)
    druh_podilu = db.Column(db.String)

class Fyzicka_Osoba(db.Model):
    __tablename__ = "fyzicke_osoby"
    id = db.Column(db.Integer, primary_key=True)
    titul_pred = db.Column(db.String)
    jmeno = db.Column(db.String)
    prijmeni = db.Column(db.String)
    titul_za = db.Column(db.String)
    datum_naroz = db.Column(MyType)

class Pravnicka_Osoba(db.Model):
    __tablename__ = "pravnicke_osoby"
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String)
    reg_cislo = db.Column(db.String)
    nazev = db.Column(db.String)