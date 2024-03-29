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

def convert_currency(my_currency):
    if my_currency == "KORUNY":
        return "Kč"
    elif my_currency == "EURA":
        return "Euro"
    else:
        return ""

def convert_contribution(my_contribution):
    if my_contribution == "KORUNY":
        return "Kč"
    elif my_contribution == "PROCENTA":
        return "%"
    elif my_contribution == "EURA":
        return "Euro"
    else:
        return ""

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

class MyCurrency(types.TypeDecorator):

    impl = types.Unicode

    def process_result_value(self, value, dialect):
        return convert_currency(value)

    def copy(self, **kw):
        return MyCurrency(self.impl.length)

class MyContribution(types.TypeDecorator):

    impl = types.Unicode

    def process_result_value(self, value, dialect):
        return convert_contribution(value)

    def copy(self, **kw):
        return MyContribution(self.impl.length)

class Predmety_Podnikani_Association(db.Model):
    __tablename__ = 'predmety_podnikani_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    predmet_podnikani_id = db.Column(db.Integer, db.ForeignKey('predmety_podnikani.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_podnikani = db.relationship("Predmet_Podnikani", back_populates="company_predmet_podnikani")
    company = db.relationship("Company", back_populates="predmet_podnikani")

class Predmety_Cinnosti_Association(db.Model):
    __tablename__ = 'predmety_cinnosti_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    predmet_cinnosti_id = db.Column(db.Integer, db.ForeignKey('predmety_cinnosti.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    predmet_cinnosti = db.relationship("Predmet_Cinnosti")
    company = db.relationship("Company")

class Ucel_Association(db.Model):
    __tablename__ = 'ucel_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    ucel_id = db.Column(db.Integer, db.ForeignKey('ucel.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    ucel = db.relationship("Ucel")
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

class Dozorci_Rada_Association(db.Model):
    __tablename__ = 'dozorci_rada_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    company = db.relationship("Company")
    pocet_clenu = db.relationship("Pocty_Clenu_DR")
    clenove = db.relationship("Dozorci_Rada_Clen_Association")

class Statutarni_Organ_Association(db.Model):
    __tablename__ = 'statutarni_organ_relation'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organy.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    statutarni_organ_text = db.relationship("Statutarni_Organy")
    company = db.relationship("Company")
    pocet_clenu = db.relationship("Pocty_Clenu_Organu")
    zpusoby_jednani = db.relationship("Zpusob_Jednani_Association")
    clenove = db.relationship("Statutarni_Organ_Clen_Association")

class Statutarni_Organ_Clen_Association(db.Model):
    __tablename__ = 'statutarni_organ_clen_relation'
    id = db.Column(db.Integer, primary_key=True)
    statutarni_organ_id = db.Column(db.Integer, db.ForeignKey('statutarni_organ_relation.id'))
    osoba_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    prav_osoba_id = db.Column(db.Integer, db.ForeignKey('pravnicke_osoby.id'))
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
    jmeno_po = db.relationship("Pravnicka_Osoba")
    statutarni_organ = db.relationship("Statutarni_Organ_Association")

class Pravnicka_Osoba(db.Model):
    __tablename__ = "pravnicke_osoby"
    id = db.Column(db.Integer, primary_key=True)
    ico = db.Column(db.String)
    reg_cislo = db.Column(db.String)
    nazev = db.Column(db.String)
    spolecnik_association = db.relationship("Spolecnici_Association")
    sole_shareholder_association = db.relationship("Jediny_Akcionar_Association")
    statut_org_association = db.relationship("Statutarni_Organ_Clen_Association")
    supervisory_board_member_association = db.relationship("Dozorci_Rada_Clen_Association")
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    adresa = db.relationship("Adresy_v2")

class Fyzicka_Osoba(db.Model):
    __tablename__ = "fyzicke_osoby"
    id = db.Column(db.Integer, primary_key=True)
    titul_pred = db.Column(db.String)
    jmeno = db.Column(db.String)
    prijmeni = db.Column(db.String)
    titul_za = db.Column(db.String)
    datum_naroz = db.Column(MyType)
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    statut_org_association = db.relationship("Statutarni_Organ_Clen_Association")
    spolecnik_association = db.relationship("Spolecnici_Association")
    prokurista_association = db.relationship("Prokurista_Association")
    sole_shareholder_association = db.relationship("Jediny_Akcionar_Association")
    supervisory_board_member_association = db.relationship("Dozorci_Rada_Clen_Association")
    ubo_association = db.relationship("Ubo")
    adresa = db.relationship("Adresy_v2")

    def get_name(self):
        joined_name = ""
        if self.titul_pred != "0" and self.titul_pred != None:
            joined_name += self.titul_pred + " "
        if self.jmeno != "0" and self.jmeno != None:
            joined_name += self.jmeno + " "
        if self.prijmeni != "0" and self.prijmeni != None:
            joined_name += self.prijmeni
        if self.titul_za != "0" and self.titul_za != None:
            joined_name += ", " +  self.titul_za
        return joined_name       
    
    def __repr__(self):
        joined_name = self.get_name()
        if self.datum_naroz != 0 and self.datum_naroz != None and self.datum_naroz != "":
            joined_name += ", nar. " + self.datum_naroz
        return joined_name

class Dozorci_Rada_Clen_Association(db.Model):
    __tablename__ = 'dr_organ_clen_relation'
    id = db.Column(db.Integer, primary_key=True)
    dozorci_rada_id = db.Column(db.Integer, db.ForeignKey('dozorci_rada_relation.id'))
    osoba_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    pravnicka_osoba_id = db.Column(db.Integer, db.ForeignKey('pravnicke_osoby.id'))
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
    jmeno_po = db.relationship("Pravnicka_Osoba")
    dozorci_rada = db.relationship("Dozorci_Rada_Association")

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
    jmeno = db.relationship("Fyzicka_Osoba", back_populates="spolecnik_association")
    oznaceni_po = db.relationship("Pravnicka_Osoba")
    podily = db.relationship("Podily_Association")
    company = db.relationship("Company")

class Podilnici_Association(db.Model):
    __tablename__ = "podilnici"
    id = db.Column(db.Integer, primary_key=True)
    podil_id = db.Column(db.Integer, db.ForeignKey('spolecnici_spolecny_podil.id'))
    podilnik_fo_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    podilnik_po_id = db.Column(db.Integer, db.ForeignKey('pravnicke_osoby.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    # text_podilnik = db.Column(db.String)
    adresa = db.relationship("Adresy_v2")
    jmeno = db.relationship("Fyzicka_Osoba")
    oznaceni_po = db.relationship("Pravnicka_Osoba")
    podily = db.relationship("Spolecny_Podil_Association")

class Uvolneny_Podil_Association(db.Model):
    __tablename__ = "spolecnici_uvolneny_podil"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    text_uvolneny_podil = db.Column(db.String)
    podily = db.relationship("Podily_Association")
    company = db.relationship("Company")

class Spolecny_Podil_Association(db.Model):
    __tablename__ = "spolecnici_spolecny_podil"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    text_spolecny_podil = db.Column(db.String)
    podily = db.relationship("Podily_Association")
    podilnici = db.relationship("Podilnici_Association")
    company = db.relationship("Company")

class Ubo(db.Model):
    __tablename__ = "ubo"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    UBO_id = db.Column(db.Integer, db.ForeignKey('fyzicke_osoby.id'))
    adresa_id = db.Column(db.Integer, db.ForeignKey('adresy_v2.id'))
    adresa = db.relationship("Adresy_v2")   
    postaveni = db.Column(db.String)
    koncovyPrijemceText = db.Column(db.String)
    skutecnymMajitelemOd = db.Column(MyType)
    jmeno = db.relationship("Fyzicka_Osoba")
    company = db.relationship("Company")    

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
    company = db.relationship("Company")

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
    company = db.relationship("Company")

class Podily_Association(db.Model):
    __tablename__ = "podily"
    id = db.Column(db.Integer, primary_key=True)
    spolecnik_id = db.Column(db.Integer, db.ForeignKey('spolecnici.id'))
    uvolneny_podil_id = db.Column(db.Integer, db.ForeignKey('spolecnici_uvolneny_podil.id'))
    spolecny_podil_id = db.Column(db.Integer, db.ForeignKey('spolecnici_spolecny_podil.id'))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    druh_podilu_id = db.Column(db.Integer, db.ForeignKey('druhy_podilu.id'))
    vklad_typ = db.Column(MyCurrency)
    vklad_text = db.Column(db.String)
    souhrn_typ = db.Column(MyContribution)
    souhrn_text = db.Column(db.String)
    splaceni_typ = db.Column(MyContribution)
    splaceni_text = db.Column(db.String)
    druh_podilu = db.relationship("Druhy_Podilu")
    
    def my_rep(self):
        podil_descr = "Vklad: " + self.vklad_text + " " + self.vklad_typ + "\n"
        podil_descr += "Splaceno: " + self.splaceni_text + " " + self.splaceni_typ
        if self.souhrn_text != "0":
            podil_descr += "\n" + "Podíl: " + self.souhrn_text + self.souhrn_typ
        if self.druh_podilu.druh_podilu != "0":
            podil_descr += "\n" + "Druh podílu: " + self.druh_podilu.druh_podilu
        return podil_descr.split("\n")

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
    criminal_record = db.relationship("Criminal_Records")
    konkurz = db.relationship("Konkurz_Events")
    predmet_podnikani = db.relationship("Predmety_Podnikani_Association")
    predmet_cinnosti = db.relationship("Predmety_Cinnosti_Association")
    ucel = db.relationship("Ucel_Association")
    zakladni_kapital =  db.relationship("Zakladni_Kapital")
    ostatni_skutecnosti = db.relationship("Ostatni_Skutecnosti")
    akcie = db.relationship("Akcie")
    obchodni_firma = db.relationship("Nazvy")
    soudni_zapis = db.relationship("Soudni_Zapisy")
    pravni_forma_text = db.relationship("Pravni_Forma_Association_v2")
    statutarni_organ_text = db.relationship("Statutarni_Organ_Association")
    dozorci_rada_text = db.relationship("Dozorci_Rada_Association")
    spolecnici = db.relationship("Spolecnici_Association")
    spolecnici_uvolneny_podil = db.relationship("Uvolneny_Podil_Association")
    spolecnici_spolecny_podil = db.relationship("Spolecny_Podil_Association")
    prokurista = db.relationship("Prokurista_Association")
    prokura_common_text = db.relationship("Prokura_Common_Text_Association")
    jediny_akcionar = db.relationship("Jediny_Akcionar_Association")
    sidlo_text = db.relationship("Sidlo_Association")
    ubo = db.relationship("Ubo")

    def current_legal_form_text(self):
        for elem in self.pravni_forma_text:
            if elem.vymaz_datum == 0:
                return elem.pravni_forma_text.predlozka_v() + " " + elem.pravni_forma_text.sesty_pad()
        return "v právnické osobě"

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
        if self.ulice != "0" and self.ulice != None:
            joined_address += self.ulice + " "
        if self.cisloText != "0" and self.cisloText != None:
            joined_address += self.cisloText + ", "   
        if self.cisloPo != 0:
            if self.ulice == "0" and self.ulice != None:
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
        if (self.castObce != "0") and (self.castObce != self.obec) and self.castObce != None:
            joined_address += self.castObce + ", "
        if self.psc != "0" and self.psc != None:
            joined_address += self.psc + " "
        if self.obec != "0" and self.obec != None:
            joined_address += self.obec
        if (self.stat != "Česká republika") and (self.stat != "Česká republika - neztotožněno") and (self.stat != "0"):
            joined_address += ", " + self.stat
        # if joined_address == "":
        #     return "adresa nedostupná"
        # else:
        return joined_address
    
    def __len__(self):
        address_text = self.__repr__()
        return len(address_text)

class Insolvency_Events(db.Model):
    __tablename__ = "insolvency_events"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    zapis_datum = db.Column(MyType)
    vymaz_datum = db.Column(MyType)
    insolvency_event = db.Column(db.String)

class Criminal_Records(db.Model):
    __tablename__ = "criminal_records"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    first_instance = db.Column(db.String)
    second_instance = db.Column(db.String)
    paragraphs = db.Column(db.String)
    penalties = db.Column(db.String)

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
    
    def my_rep(self):
        joined_zk = ""
        joined_zk += self.vklad_hodnota + " "
        
        if self.vklad_typ == "KORUNY":
            joined_zk += "Kč "
        elif self.vklad_typ == "EURA":
            joined_zk += "euro "
        
        if self.splaceni_hodnota != "0":
            joined_zk +=  "\n"
            joined_zk += "Splaceno: " + self.splaceni_hodnota + " "
            if self.splaceni_typ == "KORUNY":
                joined_zk += "Kč "
            elif self.splaceni_typ == "PROCENTA":
                joined_zk += "% "            
            elif self.splaceni_typ == "EURA":
                joined_zk += "euro "
        return joined_zk.split("\n")

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

class Ucel(db.Model):
    __tablename__ = "ucel"
    id = db.Column(db.Integer, primary_key=True)
    ucel = db.Column(db.String)
    company_ucel = db.relationship("Ucel_Association")

class Sidlo(db.Model):
    __tablename__ = "adresy"
    id = db.Column(db.Integer, primary_key=True)
    adresa_text = db.Column(db.String)

class Pravni_Formy(db.Model):
    __tablename__ = "pravni_formy"
    id = db.Column(db.Integer, primary_key=True)
    pravni_forma = db.Column(db.String)
    company_pravni_forma = db.relationship("Pravni_Forma_Association_v2")

    def predlozka_v(self):
        if self.pravni_forma == "Akciová společnost":
            return "v"
        elif self.pravni_forma == "Společnost s ručením omezeným":
            return "ve"
        elif self.pravni_forma == "Komanditní společnost":
            return "v"
        elif self.pravni_forma == "Veřejná obchodní společnost":
            return "ve"
        elif self.pravni_forma == "Družstvo":
            return "v"
        elif self.pravni_forma == "Ostatní":
            return "v"
        elif self.pravni_forma == "Evropská společnost":
            return "v"
        elif self.pravni_forma == "Spolek":
            return "ve"
        elif self.pravni_forma == "Zájmové sdružení právnických osob":
            return "v"
        elif self.pravni_forma == "Fyzická osoba - podnikatel":
            return "u"
        elif self.pravni_forma == "Zájmové sdružení právnických osob zapsané v OR":
            return "v"
        elif self.pravni_forma == "Zájmové sdružení":
            return "v"
        elif self.pravni_forma == "Zahraniční fyzická osoba":
            return "v"
        elif self.pravni_forma == "Odštěpný závod zahraniční právnické osoby":
            return "v"
        elif self.pravni_forma == "Ústav":
            return "v"
        elif self.pravni_forma == "Obecně prospěšná společnost":
            return "v"
        elif self.pravni_forma == "Společenství vlastníků jednotek":
            return "ve"
        elif self.pravni_forma == "Odborová organizace a organizace zaměstnavatelů":
            return "v"
        elif self.pravni_forma == "Organizace zaměstnavatelů":
            return "v"
        elif self.pravni_forma == "Mezinárodní nevládní organizace":
            return "v"
        elif self.pravni_forma == "Pobočný spolek":
            return "v"
        elif self.pravni_forma == "Občanské sdružení":
            return "v"
        elif self.pravni_forma == "Příspěvková organizace":
            return "v"
        elif self.pravni_forma == "Odštěpný závod zahraniční fyzické osoby":
            return "v"
        elif self.pravni_forma == "Organizační složka zahraničního nadačního fondu":
            return "v"
        elif self.pravni_forma == "Organizační složka zahraniční nadace":
            return "v"
        elif self.pravni_forma == "Pobočná odborová organizace a organizace zaměstnavatelů":
            return "v"
        elif self.pravni_forma == "Odborová organizace":
            return "v"
        elif self.pravni_forma == "Nadační fond":
            return "v"
        elif self.pravni_forma == "Nadace":
            return "v"
        elif self.pravni_forma == "Evropské hospodářské zájmové sdružení":
            return "v"
        elif self.pravni_forma == "Evropská družstevní společnost":
            return "v"
        else:
            return "v"
    
    def sesty_pad(self):
        if self.pravni_forma == "Akciová společnost":
            return "akciové společnosti"
        elif self.pravni_forma == "Společnost s ručením omezeným":
            return "společnosti s ručením omezeným"
        elif self.pravni_forma == "Komanditní společnost":
            return "komanditní společnosti"
        elif self.pravni_forma == "Veřejná obchodní společnost":
            return "veřejné obchodní společnosti"
        elif self.pravni_forma == "Družstvo":
            return "družstvu"
        elif self.pravni_forma == "Ostatní":
            return "právnické osobě"
        elif self.pravni_forma == "Evropská společnost":
            return "evropské společnosti"
        elif self.pravni_forma == "Spolek":
            return "spolku"
        elif self.pravni_forma == "Zájmové sdružení právnických osob":
            return "zájmovém sdružení právnických osob"
        elif self.pravni_forma == "Fyzická osoba - podnikatel":
            return "fyzické osoby, podnikatele"
        elif self.pravni_forma == "Zájmové sdružení právnických osob zapsané v OR":
            return "zájmovém sdružení právnických osob zapsané v OR"
        elif self.pravni_forma == "Zájmové sdružení":
            return "zájmovém sdružení"
        elif self.pravni_forma == "Zahraniční fyzická osoba":
            return "zahraniční fyzické osobě"
        elif self.pravni_forma == "Odštěpný závod zahraniční právnické osoby":
            return "odštěpném závodu zahraniční právnické osoby"
        elif self.pravni_forma == "Ústav":
            return "ústavu"
        elif self.pravni_forma == "Obecně prospěšná společnost":
            return "obecně prospěšné společnosti"
        elif self.pravni_forma == "Společenství vlastníků jednotek":
            return "společenství vlastníků jednotek"
        elif self.pravni_forma == "Odborová organizace a organizace zaměstnavatelů":
            return "odborové organizaci a organizaci zaměstnavatelů"
        elif self.pravni_forma == "Organizace zaměstnavatelů":
            return "organizaci zaměstnavatelů"
        elif self.pravni_forma == "Mezinárodní nevládní organizace":
            return "mezinárodní nevládní organizaci"
        elif self.pravni_forma == "Pobočný spolek":
            return "pobočném spolku"
        elif self.pravni_forma == "Občanské sdružení":
            return "občanském sdružení"
        elif self.pravni_forma == "Příspěvková organizace":
            return "příspěvkové organizaci"
        elif self.pravni_forma == "Odštěpný závod zahraniční fyzické osoby":
            return "odštěpném závodu zahraniční fyzické osoby"
        elif self.pravni_forma == "Organizační složka zahraničního nadačního fondu":
            return "organizační složce zahraničního nadačního fondu"
        elif self.pravni_forma == "Organizační složka zahraniční nadace":
            return "organizační složce zahraniční nadace"
        elif self.pravni_forma == "Pobočná odborová organizace a organizace zaměstnavatelů":
            return "pobočné odborové organizaci a organizaco zaměstnavatelů"
        elif self.pravni_forma == "Odborová organizace":
            return "odborové organizaci"
        elif self.pravni_forma == "Nadační fond":
            return "nadačním fondu"
        elif self.pravni_forma == "Nadace":
            return "nadaci"
        elif self.pravni_forma == "Evropské hospodářské zájmové sdružení":
            return "evropském hospodářském zájmovém sdružení"
        elif self.pravni_forma == "Evropská družstevní společnost":
            return "evropské družstevní společnosti"
        else:
            return "právnické osobě"

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
    def __repr__(self):
        joined_share_descr = "" + self.akcie_pocet + " ks "
        
        if self.akcie_typ == "KMENOVE_NA_JMENO":
            joined_share_descr += "kmenové akcie na jméno "
        elif self.akcie_typ == "KMENOVE_NA_MAJITELE":
            joined_share_descr += "kmenové akcie na majitele "
        elif self.akcie_typ == "KUSOVE_NA_JMENO":
            joined_share_descr += "kusové akcie "
        elif self.akcie_typ == "NA_JMENO":
            joined_share_descr += "akcie na jméno "
        elif self.akcie_typ == "NA_MAJITELE":
            joined_share_descr += "akcie na majitele "
        elif self.akcie_typ == "PRIORITNI_NA_JMENO":
            joined_share_descr += "prioritní akcie na jméno "
        elif self.akcie_typ == "ZAMESTNANECKE_NA_JMENO":
            joined_share_descr += "zaměstnanecké akcie na jméno "
        elif self.akcie_typ == "ZVLASTNI_PRAVA":
            joined_share_descr += "akcie se zvláštními právy "

        if self.akcie_podoba == "LISTINNA":
            joined_share_descr += "v listinné podobě "
        elif self.akcie_podoba == "ZAKNIHOVANA":
            joined_share_descr += "v zaknihované podobě "
        elif self.akcie_podoba == "IMOBILIZOVANA":
            joined_share_descr += "v imobilizované podobě "

        if self.akcie_hodnota_value != "0":
            joined_share_descr += "ve jmenovité hodnotě " + self.akcie_hodnota_value        

        if self.akcie_hodnota_typ == "KORUNY":
            joined_share_descr += "Kč"
        elif self.akcie_hodnota_typ == "EURA":
            joined_share_descr += "euro"
        return joined_share_descr

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