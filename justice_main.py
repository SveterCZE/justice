import requests
import shutil
from lxml import etree
import sqlite3
import gzip
import send2trash
import os
from datetime import datetime
import cProfile
import re
from sqlalchemy import text, exc, insert, engine

# The function opens a file and parses the extracted data into the database
def parse_to_DB(file):
    print("Processing ", str(file))
    conn = sqlite3.connect('justice_db.db')
    c = conn.cursor()
    for event, element in etree.iterparse(file, tag="Subjekt"):
        # Bugfix for companies which have been deleted but appear in the list of existing companies
        if ([element.find('vymazDatum')][0]) != None:
            continue
        else:
            ICO = get_ICO(element)
            # Vlozit prazdny radek s ICO
            insert_new_ICO(c, ICO, conn, element)
            primary_sql_key = get_primary_sql_key(c, ICO)
            # Vlozit jednolive parametry
            # insert_primary_company_figures(c, ICO, element, conn)
            insert_company_relations(c, ICO, element, conn, primary_sql_key)
            # insert_obec_relation(c, conn, ICO, element, primary_sql_key)
            find_other_properties(c, ICO, element, conn, primary_sql_key)
            element.clear()

            # subjekt_udaje.clear()
    conn.commit()
    conn.close()
    return 0

def purge_DB():
    try:
        conn = sqlite3.connect('justice.db')
        c = conn.cursor()
        c.execute("DELETE FROM adresy")
        c.execute("DELETE FROM adresy_v2")
        c.execute("DELETE FROM akcie")
        c.execute("DELETE FROM companies")
        c.execute("DELETE FROM dozorci_rada_relation")
        c.execute("DELETE FROM dr_organ_clen_relation")
        c.execute("DELETE FROM druhy_podilu")
        c.execute("DELETE FROM fyzicke_osoby")
        c.execute("DELETE FROM insolvency_events")
        c.execute("DELETE FROM jediny_akcionar")
        c.execute("DELETE FROM konkurz_events")
        c.execute("DELETE FROM nazvy")
        c.execute("DELETE FROM obce")
        c.execute("DELETE FROM obce_relation")
        c.execute("DELETE FROM osoby")
        c.execute("DELETE FROM ostatni_skutecnosti")
        c.execute("DELETE FROM pocty_clenu_DR")
        c.execute("DELETE FROM pocty_clenu_organu")
        c.execute("DELETE FROM podily")
        c.execute("DELETE FROM pravni_formy")
        c.execute("DELETE FROM pravni_formy_relation")
        c.execute("DELETE FROM predmety_cinnosti")
        c.execute("DELETE FROM predmety_cinnosti_relation")
        c.execute("DELETE FROM predmety_podnikani")
        c.execute("DELETE FROM predmety_podnikani_relation")
        c.execute("DELETE FROM prokura_common_texts")
        c.execute("DELETE FROM prokuriste")
        c.execute("DELETE FROM sidla")
        c.execute("DELETE FROM sidlo_relation")
        c.execute("DELETE FROM spolecnici")
        c.execute("DELETE FROM sqlite_sequence")
        c.execute("DELETE FROM statutarni_organ_clen_relation")
        c.execute("DELETE FROM statutarni_organ_relation")
        c.execute("DELETE FROM statutarni_organy")
        c.execute("DELETE FROM ulice")
        c.execute("DELETE FROM ulice_relation")
        c.execute("DELETE FROM zakladni_kapital")
        c.execute("DELETE FROM zapis_soudy")
        c.execute("DELETE FROM zpusoby_jednani")
        c.execute("DELETE FROM zpusoby_jednani_relation")

        conn.commit()
        conn.close()
        return 0
    except Exception as f:
        print(f)

def find_other_properties(c, ICO, element, conn, primary_sql_key):
    try:
        # my_iter = element.iter("udaje")
        my_iter = element.findall("udaje")
        for elem in my_iter:
            # my_iter2 = elem.iter("Udaj")
            my_iter2 = elem.findall("Udaj")
            for elem2 in my_iter2:
                udajTyp_name = str(get_prop(elem2, ".//udajTyp/kod"))
                if udajTyp_name == "SIDLO":
                    find_registered_office(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "NAZEV":
                    find_nazev(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "SPIS_ZN":
                    find_sp_zn(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "PRAVNI_FORMA":
                    find_pravni_forma(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "STATUTARNI_ORGAN":
                    find_statutar(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "SPOLECNIK":
                    find_spolecnik(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "PREDMET_PODNIKANI_SEKCE":
                    find_predmet_podnikani(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "PREDMET_CINNOSTI_SEKCE":
                    find_predmet_cinnosti(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "ZAKLADNI_KAPITAL":
                    find_zakladni_kapital(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "OST_SKUTECNOSTI_SEKCE":
                    find_ostatni_skutecnosti(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "AKCIE_SEKCE":
                    find_akcie(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "DOZORCI_RADA":
                    find_dozorci_rada(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "PROKURA":
                    find_prokura(c, ICO, elem2, conn, primary_sql_key, element)
                elif udajTyp_name == "AKCIONAR_SEKCE":
                    find_sole_shareholder(c, ICO, elem2, conn, primary_sql_key, element)    
                elif udajTyp_name == "INSOLVENCE_SEKCE":
                    find_active_insolvency(c, ICO, elem2, conn, primary_sql_key)
                elif udajTyp_name == "KONKURS_SEKCE":
                    find_active_konkurz(c, ICO, elem2, conn, primary_sql_key)
    except:
        pass

def find_sole_shareholder(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            zapis_datum = str(get_prop(elem, "zapisDatum"))
            vymaz_datum = str(get_prop(elem, "vymazDatum"))
            text_akcionar = str(get_prop(elem, "hodnotaUdaje/textZaOsobu/value"))                
            typ_akcionar = str(get_prop(elem, "hodnotaUdaje/T"))
            if typ_akcionar == "P":
                spol_ico = str(get_prop(elem, "osoba/ico"))
                regCislo = str(get_prop(elem, "osoba/regCislo"))
                akcionar_po_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo)
                adresa_id = find_and_store_address(c, elem)
                c.execute("INSERT into jediny_akcionar (company_id, zapis_datum, vymaz_datum, text_akcionar, akcionar_po_id, adresa_id) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, text_akcionar, akcionar_po_id, adresa_id,))
            elif typ_akcionar == "F":
                akcionar_fo_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element)
                adresa_id = find_and_store_address(c, elem)
                c.execute("INSERT into jediny_akcionar (company_id, zapis_datum, vymaz_datum, text_akcionar, akcionar_fo_id, adresa_id) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, text_akcionar, akcionar_fo_id, adresa_id,))    
    except Exception as f:
        print(f)

def find_prokura(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            typ_zapis = str(get_prop(elem, "udajTyp/kod"))
            if typ_zapis == "PROKURA_OSOBA":
                zapis_datum = str(get_prop(elem, "zapisDatum"))
                vymaz_datum = str(get_prop(elem, "vymazDatum"))
                text_prokurista = str(get_prop(elem, "hodnotaUdaje/textZaOsobu/value"))
                prokurista_fo_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element)
                adresa_id = find_and_store_address(c, elem)
                # print(ICO, zapis_datum, vymaz_datum, text_osoba, prokurista_fo_id, adresa_id)
                c.execute("INSERT INTO prokuriste (company_id, zapis_datum, vymaz_datum, prokurista_fo_id, adresa_id, text_prokurista) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, prokurista_fo_id, adresa_id, text_prokurista,))
            else:
                zapis_datum = str(get_prop(elem, "zapisDatum"))
                vymaz_datum = str(get_prop(elem, "vymazDatum"))
                prokura_text = str(get_prop(elem, "hodnotaText"))
                c.execute("INSERT INTO prokura_common_texts (company_id, zapis_datum, vymaz_datum, prokura_text) VALUES (?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, prokura_text,)) 
    except Exception as f:
        print(f)

def find_spolecnik(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        # zapis_datum = str(get_prop(elem2, "zapisDatum"))
        # vymaz_datum = str(get_prop(elem2, "vymazDatum"))
        # if vymaz_datum != "0":
        #     print(ICO, zapis_datum, vymaz_datum)
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            spolecnik_type = str(get_prop(elem, "udajTyp/kod"))
            zapis_datum = str(get_prop(elem, "zapisDatum"))
            vymaz_datum = str(get_prop(elem, "vymazDatum"))
            # spolecnik_oznaceni = str(get_prop(elem, "hlavicka"))
            spolecnik_typ =  str(get_prop(elem, "hodnotaUdaje/typ"))
            # TODO Chech these conditions, they sometimes cause a person not being stored (IC 27650081)
            # if spolecnik_type == "SPOLECNIK_OSOBA" and spolecnik_oznaceni == "Společník":
            if spolecnik_type == "SPOLECNIK_OSOBA" and spolecnik_typ == "OSOBA":
                # TODO alternativy pro None, Spolecny podil a Uvolneny podil
                text_spolecnik = str(get_prop(elem, "hodnotaUdaje/textZaOsobu/value"))
                nazev = str(get_prop(elem, "osoba/nazev"))
                # TODO Fix - make reference to type of person - some foreign persons have no ico or regCo, so they are assigned a number for a natural person
                # if spol_ico == "0" and regCislo == "0":
                if nazev == "0":
                    # I probably do not need the primary sql key
                    spolecnik_fo_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element)
                    adresa_id = find_and_store_address(c, elem)
                    c.execute("INSERT INTO spolecnici (company_id, spolecnik_fo_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, spolecnik_fo_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik,))
                    c.execute ("SELECT last_insert_rowid()")
                    spolecnik_id = c.fetchone()[0]
                    # print(ICO, spolecnik_fo_id, adresa_id)
                else:
                    spol_ico = str(get_prop(elem, "osoba/ico"))
                    regCislo = str(get_prop(elem, "osoba/regCislo"))
                    spolecnik_po_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo)
                    adresa_id = find_and_store_address(c, elem)
                    c.execute("INSERT INTO spolecnici (company_id, spolecnik_po_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, spolecnik_po_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik,))
                    c.execute ("SELECT last_insert_rowid()")
                    spolecnik_id = c.fetchone()[0]
                insert_podily(c, elem, spolecnik_id)

                    # nazev = str(get_prop(elem, "osoba/nazev"))
                    # addr = str(adresa(get_SIDLO_v3(elem)))
                    # print(ICO, nazev, spol_ico, addr)
                
    except Exception as f:
        print(f)

def insert_podily(c, elem, spolecnik_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            zapisDatum = str(get_prop(podil_elem, "zapisDatum"))
            vymazDatum = str(get_prop(podil_elem, "vymazDatum"))
            druh_podilu_id = get_druh_podilu_id(c, podil_elem)
            # druhPodilu = str(get_prop(podil_elem, "hodnotaUdaje/druhPodilu"))
            vklad_typ = str(get_prop(podil_elem, "hodnotaUdaje/vklad/typ"))
            vklad_text = str(get_prop(podil_elem, "hodnotaUdaje/vklad/textValue"))
            souhrn_typ = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/typ"))
            souhrn_text = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue"))
            splaceni_typ = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/typ"))
            splaceni_text = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue"))
            c.execute("INSERT INTO podily (spolecnik_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (?,?,?,?,?,?,?,?,?,?)", (spolecnik_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
            # print(spolecnik_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text)

    except Exception as f:
        print(f)

def get_druh_podilu_id(c, podil_elem):
    try:
        druhPodilu = str(get_prop(podil_elem, "hodnotaUdaje/druhPodilu"))
        insert_druh_podilu(c, podil_elem, druhPodilu)
        druh_podilu_id = find_druh_podilu_id(c, druhPodilu)
        return druh_podilu_id
    except Exception as f:
        print(f)

def insert_druh_podilu(c, podil_elem, druhPodilu):
    try:
        c.execute("INSERT INTO druhy_podilu (druh_podilu) VALUES (?)", (druhPodilu,))
    except:
        pass

def find_druh_podilu_id(c, druhPodilu):
    try:
        druh_podilu_id = c.execute("SELECT id FROM druhy_podilu WHERE druh_podilu = (?)", (druhPodilu,))
        druh_podilu_id = c.fetchone()[0]
        return druh_podilu_id
    except Exception as f:
        print(f) 

def find_pravnicka_osoba(c, elem, spol_ico, regCislo):
    try:
        nazev = str(get_prop(elem, "osoba/nazev"))
        insert_pravnicka_osoba(c, elem, spol_ico, regCislo, nazev)
        osoba_id = find_pravnicka_osoba_id(c, spol_ico, regCislo, nazev)
        return osoba_id
    except Exception as f:
        print(f)

def find_pravnicka_osoba_id(c, spol_ico, regCislo, nazev):
    try:
        anciallary_table_key = c.execute("SELECT id FROM pravnicke_osoby WHERE ico = (?) and reg_cislo = (?) and nazev = (?)", (spol_ico, regCislo, nazev,))
        anciallary_table_key = c.fetchone()[0]
        return anciallary_table_key
    except Exception as f:
        print(f) 

def insert_pravnicka_osoba(c, elem, spol_ico, regCislo, nazev):
    try:
        c.execute("INSERT into pravnicke_osoby (ico, reg_cislo, nazev) VALUES (?,?,?)", (spol_ico, regCislo, nazev,))
    except:
        pass

def find_pravni_forma(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        pravni_forma = str(get_prop(elem2, ".//pravniForma/nazev"))
        # print(ICO, zapis_datum, vymaz_datum, pravni_forma)
        insert_instructions = [(pravni_forma,"pravni_formy", "pravni_forma", "pravni_formy_relation")]
        for elem in insert_instructions:
            insert_into_ancillary_table(c, elem, pravni_forma)
            ancillary_table_key = get_anciallary_table_key(c, elem, pravni_forma)
            insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except:
        pass


def find_statutar(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, "zapisDatum"))
        vymaz_datum = str(get_prop(elem2, "vymazDatum"))
        oznaceni_statutar_organu = str(get_prop(elem2, ".//hlavicka"))
        # print(ICO, zapis_datum, vymaz_datum, oznaceni_statutar_organu)
        insert_instructions = [(oznaceni_statutar_organu,"statutarni_organy", "statutarni_organ_text", "statutarni_organ_relation")]
        for elem in insert_instructions:
            insert_into_ancillary_table(c, elem, oznaceni_statutar_organu)
            ancillary_table_key = get_anciallary_table_key(c, elem, oznaceni_statutar_organu)
            insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
            relationship_table_key = get_relationship_table_key(c, primary_sql_key, ancillary_table_key)
            # relationship_table_key = c.execute("SELECT id FROM statutarni_organ_relation WHERE company_id = (?) and statutarni_organ_id = (?)", (primary_sql_key,ancillary_table_key,))
            # relationship_table_key = c.fetchone()[0]
        my_iter = elem2.findall("podudaje/Udaj") 
        for elem in my_iter:
            udajTyp_name = str(get_prop(elem, "udajTyp/kod"))
            if udajTyp_name == "POCET_CLENU":
                find_pocet_clenu(c, ICO, elem, conn, relationship_table_key, element)
            elif udajTyp_name == "ZPUSOB_JEDNANI":
                find_zpusob_jednani(c, ICO, elem, conn, relationship_table_key, element)
            elif udajTyp_name == "STATUTARNI_ORGAN_CLEN":
                find_clen_statut_org(c, ICO, elem, conn, relationship_table_key, element)
            else:
                # print(str(get_prop(elem, "udajTyp/kod")))
                pass
    except Exception as f:
        print(f)

def find_dozorci_rada(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, "zapisDatum"))
        vymaz_datum = str(get_prop(elem2, "vymazDatum"))
        c.execute("INSERT into dozorci_rada_relation (company_id, zapis_datum, vymaz_datum) VALUES (?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum,))
        c.execute("SELECT id FROM dozorci_rada_relation WHERE company_id = (?) and zapis_datum = (?)", (primary_sql_key,zapis_datum,))
        relationship_table_key = c.fetchone()[0]
        my_iter = elem2.findall("podudaje/Udaj") 
        for elem in my_iter:
            udajTyp_name = str(get_prop(elem, "udajTyp/kod"))
            if udajTyp_name == "POCET_CLENU_DOZORCI_RADA":
                find_pocet_clenu_dr(c, ICO, elem, conn, relationship_table_key, element)        
            elif udajTyp_name == "DOZORCI_RADA_CLEN":
                find_clen_dr(c, ICO, elem, conn, relationship_table_key, element)
            # find_clen_dr(c, ICO, elem, conn, relationship_table_key, element)    
    except Exception as f:
        print(f)        


def find_clen_statut_org(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        funkce_statutar_organu = str(get_prop(elem, "funkce"))
        typ_osoby = str(get_prop(elem, "hodnotaText"))
        funkceOd = str(get_prop(elem, "funkceOd"))
        clenstviOd = str(get_prop(elem, "clenstviOd")) 
        funkceDo = str(get_prop(elem, "funkceDo"))
        clenstviDo = str(get_prop(elem, "clenstviDo"))
        if typ_osoby == "AngazmaFyzicke":
            osoba_id = find_fyzicka_osoba(c, ICO, elem, conn, relationship_table_key, element)
            adresa_id = find_and_store_address(c, elem)
            c.execute("INSERT into statutarni_organ_clen_relation (statutarni_organ_id, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (?,?,?,?,?,?,?,?,?,?)", (relationship_table_key, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
    except Exception as f:
        print(f)

def find_clen_dr(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        funkce_statutar_organu = str(get_prop(elem, "funkce"))
        typ_osoby = str(get_prop(elem, "hodnotaText"))
        funkceOd = str(get_prop(elem, "funkceOd"))
        clenstviOd = str(get_prop(elem, "clenstviOd")) 
        funkceDo = str(get_prop(elem, "funkceDo"))
        clenstviDo = str(get_prop(elem, "clenstviDo"))
        if typ_osoby == "AngazmaFyzicke":
            osoba_id = find_fyzicka_osoba(c, ICO, elem, conn, relationship_table_key, element)
            adresa_id = find_and_store_address(c, elem)
            c.execute("INSERT into dr_organ_clen_relation (dozorci_rada_id, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (?,?,?,?,?,?,?,?,?,?)", (relationship_table_key, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
    except Exception as f:
        print(f)

def find_fyzicka_osoba(c, ICO, elem, conn, relationship_table_key, element):
    try:
        jmeno = str(get_prop(elem, "osoba/jmeno"))
        prijmeni = str(get_prop(elem, "osoba/prijmeni"))
        datum_narozeni = str(get_prop(elem, "osoba/narozDatum"))
        titulPred = str(get_prop(elem, "osoba/titulPred"))
        titulZa = str(get_prop(elem, "osoba/titulZa"))
        insert_fyzicka_osoba(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni)
        osoba_id = find_osoba_id(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni)
        return osoba_id
    except:
        pass

def insert_fyzicka_osoba(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni):
    try:
        c.execute("INSERT into fyzicke_osoby (titul_pred, jmeno, prijmeni, titul_za, datum_naroz) VALUES (?,?,?,?,?)", (titulPred, jmeno, prijmeni, titulZa, datum_narozeni,))
    except:
        pass

def find_osoba_id(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni):
    try:
        anciallary_table_key = c.execute("SELECT id FROM fyzicke_osoby WHERE titul_pred = (?) and jmeno = (?) and prijmeni = (?) and titul_za = (?) and datum_naroz = (?)", (titulPred, jmeno, prijmeni, titulZa, datum_narozeni,))
        anciallary_table_key = c.fetchone()[0]
        return anciallary_table_key
    except Exception as f:
        print(f) 

def find_and_store_address(c, elem):
    try:
        addr = str(adresa(get_SIDLO_v3(elem)))
        insert_address(c, addr)
        address_id = find_address_id(c, addr)
        return address_id
    except Exception as f:
        print(f)

def find_address_id(c, addr):
    try:
        anciallary_table_key = c.execute("SELECT id FROM adresy WHERE adresa_text = (?)", (addr,))
        anciallary_table_key = c.fetchone()[0]
        return anciallary_table_key
    except Exception as f:
        print(f)

def get_relationship_table_key(c, primary_sql_key, ancillary_table_key):
    c.execute("SELECT id FROM statutarni_organ_relation WHERE company_id = (?) and statutarni_organ_id = (?)", (primary_sql_key,ancillary_table_key,))
    return c.fetchone()[0]

def insert_address(c, addr):
    try:
        c.execute("INSERT into adresy (adresa_text) VALUES (?)", (addr,))
    except:
        pass

# def find_statutar(c, ICO, elem2, conn, primary_sql_key, element):
#     try:
#         zapis_datum = str(get_prop(elem2, "zapisDatum"))
#         vymaz_datum = str(get_prop(elem2, "vymazDatum"))
#         oznaceni_statutar_organu = str(get_prop(elem2, ".//hlavicka"))
#         # print(ICO, zapis_datum, vymaz_datum, oznaceni_statutar_organu)
#         insert_instructions = [(oznaceni_statutar_organu,"statutarni_organy", "statutarni_organ_text", "statutarni_organ_relation")]
#         for elem in insert_instructions:
#             insert_into_ancillary_table(c, elem, oznaceni_statutar_organu)
#             ancillary_table_key = get_anciallary_table_key(c, elem, oznaceni_statutar_organu)
#             insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
#             relationship_table_key = c.execute("SELECT id FROM statutarni_organ_relation WHERE company_id = (?) and statutarni_organ_id = (?)", (primary_sql_key,ancillary_table_key,))
#             relationship_table_key = c.fetchone()[0]
#         my_iter = elem2.findall("podudaje/Udaj") 
#         for elem in my_iter:
#             udajTyp_name = str(get_prop(elem, "udajTyp/kod"))
#             if udajTyp_name == "POCET_CLENU":
#                 find_pocet_clenu(c, ICO, elem, conn, relationship_table_key, element)
#             elif udajTyp_name == "ZPUSOB_JEDNANI":
#                 find_zpusob_jednani(c, ICO, elem, conn, relationship_table_key, element)
#             elif udajTyp_name == "STATUTARNI_ORGAN_CLEN":
#                 pass
#             else:
#                 print(str(get_prop(elem, "udajTyp/kod")))
#     except Exception as f:
#         print(f)

def find_pocet_clenu(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        pocet_clenu_number = str(get_prop(elem, "hodnotaText"))
        c.execute("INSERT into pocty_clenu_organu (organ_id, pocet_clenu_value, zapis_datum, vymaz_datum) VALUES (?,?,?,?)", (relationship_table_key, pocet_clenu_number, zapis_datum, vymaz_datum,))        
        # print(ICO, zapis_datum, vymaz_datum, pocet_clenu_number)
    except Exception as f:
        print(f)

# COMBINE WITH THE ABOVE
def find_pocet_clenu_dr(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        pocet_clenu_number = str(get_prop(elem, "hodnotaText"))
        c.execute("INSERT into pocty_clenu_DR (organ_id, pocet_clenu_value, zapis_datum, vymaz_datum) VALUES (?,?,?,?)", (relationship_table_key, pocet_clenu_number, zapis_datum, vymaz_datum,))        
        # print(ICO, zapis_datum, vymaz_datum, pocet_clenu_number)
    except Exception as f:
        print(f)

def find_zpusob_jednani(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        zpusob_jednani = str(get_prop(elem, "hodnotaText"))
        insert_instructions = [(zpusob_jednani,"zpusoby_jednani", "zpusob_jednani_text", "zpusoby_jednani_relation")]
        for elem in insert_instructions:
            insert_into_ancillary_table(c, elem, zpusob_jednani)
            ancillary_table_key = get_anciallary_table_key(c, elem, zpusob_jednani)
            insert_relation_information_v2(c, elem, relationship_table_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(f)

# THIS NEEDS TO BE REFACTORED
def find_registered_office(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        sidlo = str(adresa(get_SIDLO_v3(elem2)))
        if vymaz_datum == "0":
            sidlo2(c, elem2, primary_sql_key)
            # Insert current seat into the main table
            c.execute("UPDATE companies SET sidlo = (?) WHERE id = (?)",(sidlo,primary_sql_key,))
            insert_prop(c, sidlo, conn, ICO, "sidlo")
            obec = str(get_prop(elem2, ".//adresa/obec"))
            insert_instructions = [(obec,"obce", "obec_jmeno", "obce_relation")]
            for elem in insert_instructions:
                insert_into_ancillary_table(c, elem, obec)
                ancillary_table_key = get_anciallary_table_key(c, elem, obec)
                insert_relation_information(c, elem, primary_sql_key, ancillary_table_key)
            ulice = str(get_prop(elem2, ".//adresa/ulice"))
            insert_instructions = [(ulice,"ulice", "ulice_jmeno", "ulice_relation")]
            for elem in insert_instructions:
                insert_into_ancillary_table(c, elem, ulice)
                ancillary_table_key = get_anciallary_table_key(c, elem, ulice)
                insert_relation_information(c, elem, primary_sql_key, ancillary_table_key)
        insert_instructions = [(sidlo,"adresy", "adresa_text", "sidlo_relation")]
        for elem in insert_instructions:
            insert_into_ancillary_table(c, elem, sidlo)
            ancillary_table_key = get_anciallary_table_key(c, elem, sidlo)
            insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
        return 0
    except:
        pass

def sidlo2(c, elem, primary_sql_key):
    try:
        statNazev = get_prop(elem, ".//statNazev")
        obec = get_prop(elem, ".//obec")
        ulice = get_prop(elem, ".//ulice")
        castObce = get_prop(elem, ".//castObce")
        cisloPo = get_prop(elem, ".//cisloPo")
        cisloOr = get_prop(elem, ".//cisloOr")
        psc = get_prop(elem, ".//psc")
        okres = get_prop(elem, ".//okres")
        adresaText = get_prop(elem, ".//adresaText")
        cisloEv = get_prop(elem, ".//cisloEv")
        cisloText = get_prop(elem, ".//cisloText")
        c.execute("INSERT INTO adresy_v2 (stat, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, komplet_adresa, cisloEv, cisloText, company_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText, primary_sql_key))
    except:
        pass

def find_predmet_podnikani(c, ICO, predmet_podnikani_elem, conn, primary_sql_key, element):
    try:
        my_iter = predmet_podnikani_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                # hodnota_text = str(get_prop(elem2, ".//hodnotaText"))
                insert_instructions = [(".//hodnotaText","predmety_podnikani", "predmet_podnikani", "predmety_podnikani_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText"))
                    insert_into_ancillary_table(c, elem, inserted_figure)
                    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                    insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except:
        pass

def find_predmet_cinnosti(c, ICO, predmet_cinnosti_elem, conn, primary_sql_key, element):
    try:
        my_iter = predmet_cinnosti_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                # hodnota_text = str(get_prop(elem2, ".//hodnotaText"))
                insert_instructions = [(".//hodnotaText","predmety_cinnosti", "predmet_cinnosti", "predmety_cinnosti_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText"))
                    insert_into_ancillary_table(c, elem, inserted_figure)
                    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                    insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except:
        pass

def find_sp_zn(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        soud = str(get_prop(elem2, ".//spisZn/soud/kod"))
        oddil = str(get_prop(elem2, ".//spisZn/oddil"))
        vlozka = str(get_prop(elem2, ".//spisZn/vlozka"))
        c.execute("INSERT INTO zapis_soudy (company_id, zapis_datum, vymaz_datum, oddil, vlozka, soud) VALUES(?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, oddil, vlozka, soud,))
        if vymaz_datum == "0":
            c.execute("UPDATE companies SET oddil = (?), vlozka = (?), soud = (?) WHERE id = (?)",(oddil,vlozka,soud,primary_sql_key,))
    except:
        pass

def find_nazev(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        nazev = str(get_prop(elem2, ".//hodnotaText"))
        c.execute("INSERT INTO nazvy (company_id, zapis_datum, vymaz_datum, nazev_text) VALUES(?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, nazev,))
    except:
        pass

def find_zakladni_kapital(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        vklad_typ = str(get_prop(elem2, ".//hodnotaUdaje/vklad/typ"))
        vklad_hodnota = str(get_prop(elem2, ".//hodnotaUdaje/vklad/textValue"))
        splaceni_typ = str(get_prop(elem2, ".//hodnotaUdaje/splaceni/typ"))
        splaceni_hodnota = str(get_prop(elem2, ".//hodnotaUdaje/splaceni/textValue"))
        c.execute("INSERT INTO zakladni_kapital (company_id, zapis_datum, vymaz_datum, vklad_typ, vklad_hodnota, splaceni_typ, splaceni_hodnota) VALUES(?, ?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, vklad_typ, vklad_hodnota, splaceni_typ, splaceni_hodnota,))
    except:
        pass

def find_ostatni_skutecnosti(c, ICO, ostatni_skutecnosti_elem, conn, primary_sql_key, element):
    try:
        my_iter = ostatni_skutecnosti_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                inserted_figure = str(get_prop(elem2, ".//hodnotaText"))
                c.execute("INSERT INTO ostatni_skutecnosti (company_id, zapis_datum, vymaz_datum, ostatni_skutecnost) VALUES(?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, inserted_figure,))
    except:
        pass

def find_akcie(c, ICO, ostatni_akcie_elem, conn, primary_sql_key, element):
    try:
        my_iter = ostatni_akcie_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                akcie_podoba = str(get_prop(elem2, ".//hodnotaUdaje/podoba"))
                akcie_typ = str(get_prop(elem2, ".//hodnotaUdaje/typ"))
                akcie_pocet = str(get_prop(elem2, ".//hodnotaUdaje/pocet"))
                akcie_hodnota_typ = str(get_prop(elem2, ".//hodnotaUdaje/hodnota/typ"))
                akcie_hodnota_value = str(get_prop(elem2, ".//hodnotaUdaje/hodnota/textValue"))
                akcie_text = str(get_prop(elem2, ".//hodnotaUdaje/text"))
                c.execute("INSERT INTO akcie (company_id, zapis_datum, vymaz_datum, akcie_podoba, akcie_typ, akcie_pocet, akcie_hodnota_typ, akcie_hodnota_value, akcie_text) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, akcie_podoba, akcie_typ, akcie_pocet, akcie_hodnota_typ, akcie_hodnota_value,akcie_text,))
    except:
        pass


def insert_individual_relations_v2(c, ICO, conn, primary_sql_key, zapis_datum, vymaz_datum, hodnota_text):
    insert_into_ancillary_table(c, elem, inserted_figure)
    return 0


def find_active_insolvency(c, ICO, insolvency_elem, conn, primary_sql_key):
   try:
       my_iter = insolvency_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
            #    if (str(get_prop(elem2, ".//vymazDatum"))) == "0":
                    insolvency_text = str(get_prop(elem2, ".//text"))
                    zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                    vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                    if insolvency_text != "0":
                        try:
                            c.execute("INSERT INTO insolvency_events (company_id, zapis_datum, vymaz_datum, insolvency_event) VALUES(?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, insolvency_text,))
                        except:
                            pass
   except:
       pass

def find_active_konkurz(c, ICO, konkurz_elem, conn, primary_sql_key):
   try:
       my_iter = konkurz_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
            #    if (str(get_prop(elem2, ".//vymazDatum"))) == "0":
                    konkurz_text = str(get_prop(elem2, ".//text"))
                    zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                    vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                    if konkurz_text != "0":
                        try:
                            c.execute("INSERT INTO konkurz_events (company_id, zapis_datum, vymaz_datum, konkurz_event) VALUES(?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, konkurz_text,))
                        except:
                            pass
   except:
       pass

def get_primary_sql_key(c, ICO):
    try:
        primary_key = c.execute("SELECT id FROM companies WHERE ico = (?)", (ICO,))
        primary_key = c.fetchone()
        return primary_key[0]
    except:
        return 0

    return

def insert_primary_company_figures(c, ICO, element, conn):
    # insert_instructions = [("nazev","nazev"), ("zapisDatum","zapis"), (".//udaje/Udaj/spisZn/oddil","oddil"),
    #                        (".//udaje/Udaj/spisZn/vlozka","vlozka"),(".//udaje/Udaj/spisZn/soud/kod","soud"),(str(adresa(get_SIDLO_v2(element))),"sidlo")]

    insert_instructions = [("nazev","nazev"), ("zapisDatum","zapis"), (".//udaje/Udaj/spisZn/oddil","oddil"),
                           (".//udaje/Udaj/spisZn/vlozka","vlozka"),(".//udaje/Udaj/spisZn/soud/kod","soud")]
    for elem in insert_instructions:
        insert_prop(c, get_prop(element, elem[0]), conn, ICO, elem[1])
    # Override to insert the address
    # insert_prop(c, insert_instructions[-1][0], conn, ICO, insert_instructions[-1][1])
    return 0

def insert_company_relations(c, ICO, element, conn, primary_sql_key):
    # insert_instructions = [(".//udaje/Udaj/adresa/obec","obce", "obec_jmeno", "obce_relation"), (".//udaje/Udaj/adresa/ulice","ulice", "ulice_jmeno", "ulice_relation"),
    #                        (".//udaje/Udaj/pravniForma/nazev","pravni_formy", "pravni_forma", "pravni_formy_relation")]
    insert_instructions = [(".//udaje/Udaj/pravniForma/nazev","pravni_formy", "pravni_forma", "pravni_formy_relation")]
    for elem in insert_instructions:
        insert_individual_relations(c, ICO, element, conn, primary_sql_key, elem)
    return 0

def insert_individual_relations(c, ICO, element, conn, primary_sql_key, elem):
    inserted_figure = str(get_prop(element, elem[0]))
    insert_into_ancillary_table(c, elem, inserted_figure)
    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
    insert_relation_information(c, elem, primary_sql_key, ancillary_table_key)
    return ancillary_table_key

def insert_into_ancillary_table(c, elem, inserted_figure):
    try:
        c.execute("INSERT INTO " + elem[1] + "(" + elem[2] + ") VALUES(?)", (inserted_figure,))
    except:
        pass

def get_anciallary_table_key(c, elem, inserted_figure):
    try:
        anciallary_table_key = c.execute("SELECT id FROM " + elem[1] + " WHERE " + elem[2] + " = (?)", (inserted_figure,))
        anciallary_table_key = c.fetchone()[0]
        return anciallary_table_key
    except Exception as f:
        print(f)
 
def insert_relation_information(c, elem, primary_sql_key, ancillary_table_key):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(?, ?)", (primary_sql_key, ancillary_table_key,))
    except:
        pass
    return 0

def insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(NULL, ?, ?, ?, ?)", (primary_sql_key, ancillary_table_key,zapis_datum, vymaz_datum,))
    except Exception as f:
        print(f)
    return 0

def insert_obec_relation(c, conn, ICO, element, primary_sql_key):
    obec = str(get_prop(element, ".//udaje/Udaj/adresa/obec"))
    # Insert a municipality into a table with municipalites
    try:
        c.execute("INSERT INTO obce (obec_jmeno) VALUES(?)", (obec,))
    except:
        pass
    # Get municipality sql_id
    try:
        municipality_key = c.execute("SELECT id FROM obce WHERE obec_jmeno = (?)", (obec,))
        municipality_key = c.fetchone()[0]
    except:
        print("Nepovedlo se")
    # Establish a relational link
    try:
        c.execute("INSERT INTO obec_relation VALUES(?, ?)", (primary_sql_key, municipality_key,))
    except:
        pass

    return

def zkusit_najit_vsechny_osoby(element):
    stat_list = element.iter('osoba')
    temp_osoby = []
    for elem in stat_list:
        try:
            osoba_temp = ""
            osoba_temp += get_prop(element, ".//jmeno") + " "
            osoba_temp += get_prop(element, ".//prijmeni") + ", nar. "
            osoba_temp += get_prop(element, ".//narozDatum")
            temp_osoby.append(osoba_temp)
        except:
            pass
    return temp_osoby


def zkusit_najit_vsechny_adresy(element):
    stat_list = element.iter('adresa')
    temp_adresy = []
    for elem in stat_list:
        temp_adresy.append(str(adresa(get_SIDLO_v3(elem))))
    return temp_adresy

def find_business(element):
    subjekt_udaje = element.findall('.//Udaj')
    for udaj in subjekt_udaje:
        udaje_spolecnosti = udaj.findall(".//kod")
        if "PREDMET_PODNIKANI_SEKCE" in udaje_spolecnosti[0].text:
            predmety2 = [elem.text.replace(u'\xa0', u' ') for elem in udaj.iterfind(".//hodnotaText")]
            return predmety2
            # TODO - Filter areas that are no longer relevant

def insert_obec(c, obec, conn, ICO, sql_id):
    try:
        c.execute("INSERT INTO obce (obec_jmeno) VALUES(?)", (obec,))
    except:
        pass

def insert_adresa(c, adresa, conn, ICO, sql_id):
    try:
        c.execute("INSERT INTO adresy (adresa_jmeno) VALUES(?)", (adresa,))
    except:
        pass

def insert_osoba(c, osoba, conn, ICO, sql_id):
    try:
        c.execute("INSERT INTO osoby (osoba_jmeno) VALUES(?)", (osoba,))
    except:
        pass


def insert_ulice(c, ulice, conn, ICO, sql_id):
    try:
        c.execute("INSERT INTO ulice (ulice_jmeno) VALUES(?)", (ulice,))
    except:
        pass

def insert_prop_v2(c, prop, conn, ICO, column, table, sql_id):
    # print(column, prop, ICO)
    # c.execute("UPDATE companies SET (" + column + ") = (?) WHERE ico = (?)", (prop, ICO,))
    if prop != None:
        for elem in prop:
            # print(sql_id)
            c.execute("INSERT INTO predmety_podnikani (company_id, predmet_podnikani) VALUES(?,?)", (sql_id, elem,))
                # c.execute("UPDATE (%s) SET (%s, %s) = (?)" % (table, sql_id, elem), (prop, ICO,))


# Function to attempt to insert a placeholder for a new company based on ICO
def insert_new_ICO(c, ICO, conn, element):

    try:
        datum_zapis = str(get_prop(element, "zapisDatum"))
        nazev = str(get_prop(element, "nazev"))
        c.execute("INSERT INTO companies (ico, zapis, nazev) VALUES (?,?,?);", (ICO,datum_zapis,nazev,))
        return c.lastrowid

    # c.execute("INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ICO, "", "", "", "", "", "", "", "", "", ""))

    #     # conn.commit()
    except:
        pass

def get_ICO(element):
    try:
        return element.find('ico').text
        # return [element.find('ico')][0].text
    except:
        return "00000000"

def get_prop(element, prop):
    try:
        return element.find(prop).text
    except:
        return "0"

    # return [element.find(prop)][0].text

def insert_prop(c, prop, conn, ICO, column):
    # print(column, prop, ICO)
    # c.execute("UPDATE companies SET (" + column + ") = (?) WHERE ico = (?)", (prop, ICO,))
    try:
        c.execute("UPDATE companies SET (%s) = (?) WHERE ico = (?)" % (column), (prop, ICO,))
    except Exception as e:
        print(e)

# def insert_prop(c, prop, conn, ICO, column):
#     # print(column, prop, ICO)
#     # c.execute("UPDATE companies SET (" + column + ") = (?) WHERE ico = (?)", (prop, ICO,))
#     try:
#         c.execute("UPDATE companies SET (%s) = (?) WHERE ico = (?)" % (column), (prop, ICO,))
#     except:
#         pass

def get_SIDLO_v2(element):
    address_field = []
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/statNazev"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/obec"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/ulice"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/castObce"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/cisloPo"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/cisloOr"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/psc"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/okres"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/adresaText"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/cisloEv"))
    address_field.append(get_prop(element, ".//udaje/Udaj/adresa/cisloText"))
    if address_field[0] == "Česká republika - neztotožněno":
        address_field[0] = "Česká republika"
    for i in range(len(address_field)):
        if address_field[i] == "0":
            address_field[i] = None
    return address_field

def get_SIDLO_v3(element):
    address_field = []
    address_field.append(get_prop(element, ".//statNazev"))
    address_field.append(get_prop(element, ".//obec"))
    address_field.append(get_prop(element, ".//ulice"))
    address_field.append(get_prop(element, ".//castObce"))
    address_field.append(get_prop(element, ".//cisloPo"))
    address_field.append(get_prop(element, ".//cisloOr"))
    address_field.append(get_prop(element, ".//psc"))
    address_field.append(get_prop(element, ".//okres"))
    address_field.append(get_prop(element, ".//adresaText"))
    address_field.append(get_prop(element, ".//cisloEv"))
    address_field.append(get_prop(element, ".//cisloText"))
    if address_field[0] == "Česká republika - neztotožněno":
        address_field[0] = "Česká republika"
    for i in range(len(address_field)):
        if address_field[i] == "0":
            address_field[i] = None
    return address_field


class adresa(object):
    def __init__(self, adresa):
        self.stat = adresa[0]
        self.obec = adresa[1]
        self.ulice = adresa[2]
        self.castObce = adresa[3]
        self.cisloPo = adresa[4]
        self.cisloOr = adresa[5]
        self.psc = adresa[6]
        self.okres = adresa[7]
        self.komplet_adresa = adresa[8]
        self.cisloEv = adresa[9]
        self.cisloText = adresa[10]

    def __str__ (self):
        try:
            # if self.obec == "-":
            #     return("Neznama adresa")
            if self.komplet_adresa != None:
                if self.stat != None:
                    return str(self.komplet_adresa + " " + self.stat)
                else:
                    return str(self.komplet_adresa)
            # if self.obec == None:
            #     return("Neznama adresa")
            if self.cisloText != None:
                if self.ulice == None:
                    if self.psc != None:
                        return str(self.cisloText + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)
                    else:
                        return str(self.cisloText + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.obec + ", " + self.stat)
                if self.okres == None and self.castObce != None:
                        if self.psc != None:
                            return str(self.obec + " - " + self.castObce + ", " + self.ulice + " " + self.cisloText + ", PSČ " + self.psc)
                        else:
                            return str(self.obec + " - " + self.castObce + ", " + self.ulice + " " + self.cisloText)
                if self.okres == None and self.castObce == None and self.psc != None:
                    return str(self.obec + ", " + self.ulice + " " + self.cisloText + ", PSČ " + self.psc)
                if self.castObce == None and self.psc == None:
                    return str(self.obec + ", " + self.ulice + " " + self.cisloText)
                else:
                    if self.psc != None and self.ulice == None:
                        return str(self.obec + " " + self.cisloText + " " + "okres " +  self.okres + ", PSČ " + self.psc)
                    elif self.ulice == None:
                        return str(self.obec + " " + self.cisloText + " " + "okres " +  self.okres)
                    elif self.obec != None and self.ulice != None and self.psc != None:
                        return str(self.obec + ", " + self.ulice + " " + self.cisloText + ", PSČ " + self.psc)
                    elif self.obec != None and self.ulice != None:
                        return str(self.obec + ", " + self.ulice + " " + self.cisloText)
            if self.ulice != None :
                if self.cisloOr != None:
                    if self.cisloPo == None:
                        return str(self.ulice + " " + self.cisloOr + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)
                    elif self.psc != None:
                        return str(self.ulice + " " + self.cisloPo + "/" + self.cisloOr + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)
                    else:
                        return str(self.ulice + " " + self.cisloPo + "/" + self.cisloOr + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.obec + ", " + self.stat)
                if self.cisloPo == None:
                    if self.cisloEv == None:
                        if self.psc != None:
                            return str(self.obec + ", " + self.ulice + "" + srovnat_obec_cast(self.obec, self.castObce) + ", PSČ " + self.psc + " " + self.stat)
                        else:
                            return str(self.obec + ", " + self.ulice + "" + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.stat)
                    else:
                        return str(self.ulice + " č.ev. " + self.cisloEv + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)
                else:
                    if self.psc != None:
                        return str(self.ulice + " " + self.cisloPo + "" + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)
                    else:
                        return str(self.ulice + " " + self.cisloPo + "" + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.obec + ", " + self.stat)

            if self.cisloPo == None and self.cisloEv != None:
                return str(self.obec + " č.ev. " + self.cisloEv + ", " + self.psc + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.obec + ", " + self.stat)

            if self.cisloPo != None:
                return str("č.p. " + self.cisloPo + ", " + self.psc + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.obec + ", " + self.stat)

            if self.cisloPo == None and self.cisloEv == None and self.ulice == None:
                return (self.obec + " " + self.stat)

        except TypeError:
              temp_adr = []
              if self.ulice != None:
                  temp_adr.append(self.ulice)

              if self.obec != None:
                  temp_adr.append(self.obec)

              if self.castObce != None:
                  temp_adr.append(self.castObce)

              if self.cisloPo != None:
                  temp_adr.append(self.cisloPo)

              if self.cisloOr != None:
                  temp_adr.append(self.cisloOr)

              if self.psc != None:
                  temp_adr.append(self.psc)

              if self.okres != None:
                  temp_adr.append(self.okres)

              if self.cisloEv != None:
                  temp_adr.append(self.cisloEv)

              if self.cisloText != None:
                  temp_adr.append(self.cisloText)

              if self.stat != None:
                  temp_adr.append(self.stat)

              listToStr = ' '.join([str(elem) for elem in temp_adr])

              return listToStr

def srovnat_obec_cast(obec, cast_obce):
    if obec == cast_obce:
        return str("")
    elif cast_obce == None:
        return str("")
    else:
        return str(", " + cast_obce)

def general_update(method):
    typy_po = ["as", "sro", "vos", "ks", "dr", "zajzdrpo", "zahrfos", "ustav", "svj", "spolek", "prisp", "pobspolek",
                  "oszpo", "osznadf", "osznad", "orgzam", "odbororg", "nadf", "nad", "evrspol", "evrhzs", "evrdrspol"]
    soudy = ["praha", "plzen", "brno", "ceske_budejovice", "hradec_kralove", "ostrava", "usti_nad_labem"]
    # typy_po = ["as"]
    # soudy = ["ostrava"]

    rok = str(datetime.now().year)
    for osoba in typy_po:
        for soud in soudy:
            if method == "down":
                update_data(osoba + "-full-" + soud + "-" + rok + ".xml.gz")
            elif method == "db_update":
                try:
                    parse_to_DB(os.path.join(str(os.getcwd()), "data", osoba) + "-full-" + soud + "-" + rok + ".xml")
                except:
                    pass

def update_data(filename):
    source = "https://dataor.justice.cz/api/file/" + filename
    # temp_file = "D:\\Programovani\\Moje vymysly\\Justice\\data\\temp-" + filename
    temp_file = os.path.join(str(os.getcwd()), "data", "temp-" + filename)
    # temp_file = str(os.getcwd()) + "\\data\\temp-" + filename
    downloaded_OR = downloadOR(source)
    if downloaded_OR != None:
        save_temp_file(downloaded_OR, temp_file)
        unzip_file(filename[:-3], temp_file)
        delete_archive(temp_file)
        parse_check = parseOR(temp_file[:-3])
        if parse_check == True:
            update_main_file(filename[:-3], temp_file[:-3])
            # delete_archive(temp_file[:-3])
        else:
            delete_archive(temp_file[:-3])


def downloadOR(source):
    download = requests.get(source, stream = True)
    try:
        print("Downloading file ", source)
        download.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s" % (exc))
        return None
    return download

def parseOR(download):
    print("Parsing the file!")
    try:
        for event, element in etree.iterparse(download):
            element.clear()
        print("Parsing succsessful!")
    except:
        print("Parsing failed!")
        return False
    return True

def save_temp_file(download, temp_file):
    temp_file = open(temp_file, "wb")
    for chunk in download.iter_content(1000000):
        temp_file.write(chunk)
    temp_file.close()

def update_main_file(filename, temp_file):
    shutil.move(temp_file, os.path.join(str(os.getcwd()), "data", filename))

def delete_temp_file(temp_file):
    temp_file = open(temp_file, "w")
    temp_file.write("0")
    temp_file.close()

def unzip_file(filename, temp_file):
    with gzip.open(temp_file, 'rb') as f_in:
        with open(os.path.join(str(os.getcwd()), "data", "temp-" + filename), "wb") as f_out:
        # with open(str(os.getcwd()) + "\\data\\temp-" + filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def delete_archive(file):
    send2trash.send2trash(file)

def create_DB(db_file):
    create_DB_file(db_file)
    conn = create_connection(db_file)
    create_tables(conn)
    create_indices(conn)
    conn.commit()
    conn.close()

def create_DB_file(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn

def create_tables(conn):
    companies = """ CREATE TABLE "companies" (
	"id"	INTEGER,
	"ico"	TEXT NOT NULL UNIQUE,
	"nazev"	TEXT,
	"zapis"	DATE,
	"sidlo"	TEXT,
	"oddil"	TEXT,
	"vlozka"	TEXT,
	"soud"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
    ); """
    
    adresy = """ CREATE TABLE "adresy" (
	"id"	INTEGER NOT NULL,
	"adresa_text"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
    ); """

    adresy_v2 = """ CREATE TABLE "adresy_v2" (
	"id"	INTEGER NOT NULL UNIQUE,
	"stat"	TEXT,
	"obec"	TEXT,
	"ulice"	TEXT,
	"castObce"	TEXT,
	"cisloPo"	INTEGER,
	"cisloOr"	INTEGER,
	"psc"	TEXT,
	"okres"	TEXT,
	"komplet_adresa"	TEXT,
	"cisloEv"	INTEGER,
	"cisloText"	TEXT,
	"company_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("stat","obec","ulice","castObce","cisloPo","cisloOr","psc","okres","komplet_adresa","cisloEv","cisloText")
    ); """

    akcie = """ CREATE TABLE "akcie" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"akcie_podoba"	TEXT,
	"akcie_typ"	TEXT,
	"akcie_pocet"	TEXT,
	"akcie_hodnota_typ"	TEXT,
	"akcie_hodnota_value"	TEXT,
	"akcie_text"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    dr_relation = """ CREATE TABLE "dozorci_rada_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    dr_organ_clen_relation = """ CREATE TABLE "dr_organ_clen_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"dozorci_rada_id"	INTEGER NOT NULL,
	"osoba_id"	INTEGER NOT NULL,
	"adresa_id"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"funkce_od"	DATE,
	"funkce_do"	DATE,
	"clenstvi_od"	DATE,
	"clenstvi_do"	DATE,
	"funkce"	TEXT,
	FOREIGN KEY("adresa_id") REFERENCES "adresy"("id"),
	FOREIGN KEY("dozorci_rada_id") REFERENCES "dozorci_rada_relation"("id"),
	FOREIGN KEY("osoba_id") REFERENCES "fyzicke_osoby"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    druhy_podilu = """ CREATE TABLE "druhy_podilu" (
	"id"	INTEGER NOT NULL UNIQUE,
	"druh_podilu"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    fyzicke_osoby = """ CREATE TABLE "fyzicke_osoby" (
	"id"	INTEGER NOT NULL UNIQUE,
	"titul_pred"	TEXT,
	"jmeno"	TEXT,
	"prijmeni"	TEXT,
	"titul_za"	TEXT,
	"datum_naroz"	TEXT,
	UNIQUE("titul_pred","jmeno","prijmeni","titul_za","datum_naroz"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    insolvency_events = """ CREATE TABLE "insolvency_events" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	TEXT NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"insolvency_event"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    jediny_akcionar = """ CREATE TABLE "jediny_akcionar" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"text_akcionar"	TEXT,
	"akcionar_po_id"	INTEGER,
	"akcionar_fo_id"	INTEGER,
	"adresa_id"	INTEGER,
	FOREIGN KEY("adresa_id") REFERENCES "adresy"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("akcionar_po_id") REFERENCES "pravnicke_osoby"("id"),
	FOREIGN KEY("akcionar_fo_id") REFERENCES "fyzicke_osoby"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    konkurz_events = """ CREATE TABLE "konkurz_events" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	TEXT NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"konkurz_event"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    nazvy = """ CREATE TABLE "nazvy" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"nazev_text"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    obce = """ CREATE TABLE "obce" (
	"id"	INTEGER NOT NULL,
	"obec_jmeno"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    obce_relation = """ CREATE TABLE "obce_relation" (
	"company_id"	INTEGER NOT NULL UNIQUE,
	"obec_id"	INTEGER NOT NULL,
	FOREIGN KEY("obec_id") REFERENCES "obce"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    osoby = """ CREATE TABLE "osoby" (
	"id"	INTEGER NOT NULL,
	"osoba_jmeno"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    ostatni_skutecnosti = """ CREATE TABLE "ostatni_skutecnosti" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"ostatni_skutecnost"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    pocty_clenu_DR = """ CREATE TABLE "pocty_clenu_DR" (
	"id"	INTEGER NOT NULL UNIQUE,
	"organ_id"	INTEGER NOT NULL,
	"pocet_clenu_value"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("organ_id") REFERENCES "dozorci_rada_relation"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    pocty_clenu_organu = """ CREATE TABLE "pocty_clenu_organu" (
	"id"	INTEGER NOT NULL UNIQUE,
	"organ_id"	INTEGER NOT NULL,
	"pocet_clenu_value"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	FOREIGN KEY("organ_id") REFERENCES "statutarni_organ_relation"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    podily = """ CREATE TABLE "podily" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spolecnik_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"druh_podilu_id"	INTEGER,
	"vklad_typ"	TEXT,
	"vklad_text"	TEXT,
	"souhrn_typ"	TEXT,
	"souhrn_text"	TEXT,
	"splaceni_typ"	TEXT,
	"splaceni_text"	TEXT,
	FOREIGN KEY("druh_podilu_id") REFERENCES "druhy_podilu"("id"),
	FOREIGN KEY("spolecnik_id") REFERENCES "spolecnici"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    pravni_formy = """ CREATE TABLE "pravni_formy" (
	"id"	INTEGER NOT NULL,
	"pravni_forma"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    pravni_formy_relation = """ CREATE TABLE "pravni_formy_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"pravni_forma_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("pravni_forma_id") REFERENCES "pravni_formy"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    pravnicke_osoby = """ CREATE TABLE "pravnicke_osoby" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ico"	INTEGER,
	"reg_cislo"	INTEGER,
	"nazev"	TEXT,
	UNIQUE("ico","reg_cislo","nazev"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    predmety_cinnosti = """ CREATE TABLE "predmety_cinnosti" (
	"id"	INTEGER NOT NULL,
	"predmet_cinnosti"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    predmety_cinnosti_relation = """ CREATE TABLE "predmety_cinnosti_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"predmet_cinnosti_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("predmet_cinnosti_id") REFERENCES "predmety_cinnosti"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    prdmety_podnikani = """ CREATE TABLE "predmety_podnikani" (
	"id"	INTEGER NOT NULL,
	"predmet_podnikani"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    predmety_podnikani_relation = """ CREATE TABLE "predmety_podnikani_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"predmet_podnikani_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("predmet_podnikani_id") REFERENCES "predmety_podnikani"("id")
); """

    prokura_common_texts = """ CREATE TABLE "prokura_common_texts" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"prokura_text"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    prokuriste = """ CREATE TABLE "prokuriste" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"prokurista_fo_id"	INTEGER,
	"adresa_id"	INTEGER,
	"text_prokurista"	TEXT,
	FOREIGN KEY("adresa_id") REFERENCES "adresy"("id"),
	FOREIGN KEY("prokurista_fo_id") REFERENCES "fyzicke_osoby"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    sidla = """ CREATE TABLE "sidla" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"sidlo_adresa"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    sidlo_relation = """ CREATE TABLE "sidlo_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"sidlo_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("sidlo_id") REFERENCES "adresy"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    spolecnici = """ CREATE TABLE "spolecnici" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"spolecnik_fo_id"	INTEGER,
	"spolecnik_po_id"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"adresa_id"	INTEGER,
	"text_spolecnik"	TEXT,
	FOREIGN KEY("adresa_id") REFERENCES "adresy"("id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("spolecnik_fo_id") REFERENCES "fyzicke_osoby"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    statutarni_organ_clen_relation = """ CREATE TABLE "statutarni_organ_clen_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"statutarni_organ_id"	INTEGER NOT NULL,
	"osoba_id"	INTEGER,
	"adresa_id"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"funkce_od"	DATE,
	"funkce_do"	DATE,
	"clenstvi_od"	DATE,
	"clenstvi_do"	DATE,
	"funkce"	TEXT,
	FOREIGN KEY("osoba_id") REFERENCES "fyzicke_osoby"("id"),
	FOREIGN KEY("statutarni_organ_id") REFERENCES "statutarni_organ_relation"("id"),
	FOREIGN KEY("adresa_id") REFERENCES "adresy"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    statutarni_organ_relation = """ CREATE TABLE "statutarni_organ_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"statutarni_organ_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("statutarni_organ_id") REFERENCES "statutarni_organy"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    statutarni_organy = """ CREATE TABLE "statutarni_organy" (
	"id"	INTEGER NOT NULL UNIQUE,
	"statutarni_organ_text"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    ulice = """ CREATE TABLE "ulice" (
	"id"	INTEGER NOT NULL,
	"ulice_jmeno"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    ulice_relation = """ CREATE TABLE "ulice_relation" (
	"company_id"	INTEGER NOT NULL UNIQUE,
	"ulice_id"	INTEGER NOT NULL,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("ulice_id") REFERENCES "ulice"("id")
); """

    zakladni_kapital = """ CREATE TABLE "zakladni_kapital" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"vklad_typ"	TEXT,
	"vklad_hodnota"	TEXT,
	"splaceni_typ"	TEXT,
	"splaceni_hodnota"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    zapis_soudy = """ CREATE TABLE "zapis_soudy" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"oddil"	TEXT,
	"vlozka"	TEXT,
	"soud"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """

    zpusoby_jednani = """ CREATE TABLE "zpusoby_jednani" (
	"id"	INTEGER NOT NULL UNIQUE,
	"zpusob_jednani_text"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    zpusoby_jednani_relation = """ CREATE TABLE "zpusoby_jednani_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"statutarni_organ_id"	INTEGER NOT NULL,
	"zpusob_jednani_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("zpusob_jednani_id") REFERENCES "zpusoby_jednani"("id"),
	FOREIGN KEY("statutarni_organ_id") REFERENCES "statutarni_organ_relation"("id")
); """

    list_of_tables = [companies, adresy, adresy_v2, akcie, dr_relation, dr_organ_clen_relation, druhy_podilu, fyzicke_osoby, insolvency_events, 
    jediny_akcionar, konkurz_events, nazvy, obce, obce_relation, osoby, ostatni_skutecnosti, pocty_clenu_DR, pocty_clenu_organu, podily, pravni_formy, 
    pravni_formy_relation, pravnicke_osoby, predmety_cinnosti, predmety_cinnosti_relation, prdmety_podnikani, predmety_podnikani_relation,
    prokura_common_texts, prokuriste, sidla, sidlo_relation, spolecnici, statutarni_organ_clen_relation, statutarni_organ_relation, statutarni_organy, ulice, 
    ulice_relation, zakladni_kapital, zapis_soudy, zpusoby_jednani, zpusoby_jednani_relation]
    for elem in list_of_tables:
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(e)

def create_indices(conn):
    companies = """ CREATE INDEX "companies index" ON "companies" (
	"id",
	"ico",
	"nazev",
	"zapis",
	"sidlo",
	"oddil",
	"vlozka",
	"soud"
); """

    adresy = """ CREATE INDEX "index adresy" ON "adresy" (
	"adresa_text",
	"id"
); """

    adresa_text = """ CREATE INDEX "index adresy_adresa_text" ON "adresy" (
	"adresa_text"
); """

    akcie = """ CREATE INDEX "index akcie" ON "akcie" (
	"id",
	"company_id",
	"zapis_datum",
	"vymaz_datum",
	"akcie_podoba",
	"akcie_typ",
	"akcie_pocet",
	"akcie_hodnota_typ",
	"akcie_hodnota_value",
	"akcie_text"
); """

    akcionari = """ CREATE INDEX "index akcionari" ON "jediny_akcionar" (
	"id",
	"company_id",
	"zapis_datum",
	"vymaz_datum",
	"text_akcionar",
	"akcionar_po_id",
	"akcionar_fo_id",
	"adresa_id"
); """

    companies_ico = """ CREATE INDEX "index companies_ico" ON "companies" (
	"ico"
); """

    companies_nazvy = """ CREATE INDEX "index companies_nazvy" ON "companies" (
	"nazev"
); """

    companies_vznik = """ CREATE INDEX "index companies_vznik" ON "companies" (
	"zapis"
); """

    dr_clen_relation = """ CREATE INDEX "index dr clen relation" ON "dr_organ_clen_relation" (
	"dozorci_rada_id",
	"id",
	"osoba_id",
	"adresa_id",
	"zapis_datum",
	"vymaz_datum",
	"funkce_od",
	"funkce_do",
	"clenstvi_od",
	"clenstvi_do",
	"funkce"
); """

    dr_relation = """ CREATE INDEX "index dr relation" ON "dozorci_rada_relation" (
	"id",
	"company_id",
	"zapis_datum",
	"vymaz_datum"
); """

    dr_relation2 = """ CREATE INDEX "index dr relation v2" ON "dozorci_rada_relation" (
	"company_id",
	"id",
	"zapis_datum",
	"vymaz_datum"
); """

    insolvency_events = """ CREATE INDEX "index insolvency events" ON "insolvency_events" (
	"company_id",
	"vymaz_datum",
	"insolvency_event",
	"zapis_datum",
	"id"
); """

    insolvency2 = """ CREATE INDEX "index insolvency2" ON "insolvency_events" (
	"company_id"
); """

    jmena_firem = """ CREATE INDEX "index jmena firem" ON "companies" (
	"nazev"
); """

    nazvy_nazev_text = """ CREATE INDEX "index nazvy_nazev_text" ON "nazvy" (
	"nazev_text"
); """

    obce = """ CREATE INDEX "index obce" ON "obce" (
	"id",
	"obec_jmeno"
); """

    obec_jmeno = """ CREATE INDEX "index obec_jmeno" ON "obce" (
	"obec_jmeno"
); """

    osoby = """ CREATE INDEX "index osoby" ON "osoby" (
	"id",
	"osoba_jmeno"
); """

    ostatni_skutecnosti2 = """ CREATE INDEX "index ostatni skutecnosti v2" ON "ostatni_skutecnosti" (
	"company_id",
	"id",
	"zapis_datum",
	"vymaz_datum",
	"ostatni_skutecnost"
); """

    pocty_clenu_organ = """ CREATE INDEX "index pocty clenu org_v2" ON "pocty_clenu_organu" (
	"organ_id",
	"id",
	"pocet_clenu_value",
	"zapis_datum",
	"vymaz_datum"
); """

    podily = """ CREATE INDEX "index podily" ON "podily" (
	"id",
	"spolecnik_id",
	"zapis_datum",
	"vymaz_datum",
	"druh_podilu_id",
	"vklad_typ",
	"vklad_text",
	"souhrn_typ",
	"souhrn_text",
	"splaceni_typ",
	"splaceni_text"
); """

    podily_spolecnik = """ CREATE INDEX "index podily spolecnik_id" ON "podily" (
	"spolecnik_id",
	"id",
	"zapis_datum",
	"vymaz_datum",
	"druh_podilu_id",
	"vklad_typ",
	"vklad_text",
	"souhrn_typ",
	"souhrn_text",
	"splaceni_typ",
	"splaceni_text"
); """

    pravni_formy = """ CREATE INDEX "index pravni_formy" ON "pravni_formy" (
	"pravni_forma"
); """

    predmety_cinnosti_relation_v2 = """ CREATE INDEX "index predmety cinnosti relation v2" ON "predmety_cinnosti_relation" (
	"company_id",
	"id",
	"predmet_cinnosti_id",
	"zapis_datum",
	"vymaz_datum"
); """

    predmety_podnikani_relation = """ CREATE INDEX "index predmety podnikani relation v2" ON "predmety_podnikani_relation" (
	"company_id",
	"id",
	"predmet_podnikani_id",
	"zapis_datum",
	"vymaz_datum"
); """

    predmety_cinnosti = """ CREATE INDEX "index predmety_cinnosti" ON "predmety_cinnosti" (
	"predmet_cinnosti"
); """

    predmety_podnikani = """ CREATE INDEX "index predmety_podnikani" ON "predmety_podnikani" (
	"predmet_podnikani"
); """

    prokuriste = """ CREATE INDEX "index prokuriste" ON "prokuriste" (
	"id",
	"company_id",
	"zapis_datum",
	"vymaz_datum",
	"prokurista_fo_id",
	"adresa_id",
	"text_prokurista"
); """

    sidlo = """ CREATE INDEX "index sidlo" ON "sidla" (
	"company_id",
	"vymaz_datum",
	"sidlo_adresa",
	"id",
	"zapis_datum"
); """

    sidlo_relation = """ CREATE INDEX "index sidlo relation" ON "sidlo_relation" (
	"id",
	"company_id",
	"sidlo_id",
	"zapis_datum",
	"vymaz_datum"
); """

    sidlo2 = """ CREATE INDEX "index sidlo2" ON "sidla" (
	"company_id"
); """

    soudni_zapis = """ CREATE INDEX "index soudni_zapis" ON "zapis_soudy" (
	"company_id",
	"vymaz_datum",
	"oddil",
	"vlozka",
	"soud",
	"zapis_datum",
	"id"
); """

    spolecnici = """ CREATE INDEX "index spolecnici" ON "spolecnici" (
	"id",
	"company_id",
	"spolecnik_fo_id",
	"spolecnik_po_id",
	"zapis_datum",
	"vymaz_datum",
	"adresa_id",
	"text_spolecnik"
); """

    spolecnici2 = """ CREATE INDEX "index spolecnici 2" ON "spolecnici" (
	"company_id",
	"id",
	"spolecnik_fo_id",
	"spolecnik_po_id",
	"zapis_datum",
	"vymaz_datum",
	"adresa_id",
	"text_spolecnik"
); """

    statutarni_organy = """ CREATE INDEX "index statutarn_organy" ON "statutarni_organy" (
	"id",
	"statutarni_organ_text"
); """

    statutarni_organy_relation = """ CREATE INDEX "index statutarni organ relation" ON "statutarni_organ_relation" (
	"id",
	"company_id",
	"statutarni_organ_id",
	"zapis_datum",
	"vymaz_datum"
); """

    statutarni_organy_relation_v2 = """ CREATE INDEX "index statutarni organ relation v2" ON "statutarni_organ_clen_relation" (
	"statutarni_organ_id",
	"id",
	"osoba_id",
	"adresa_id",
	"zapis_datum",
	"vymaz_datum",
	"funkce_od",
	"funkce_do",
	"clenstvi_od",
	"clenstvi_do",
	"funkce"
); """

    v2 = """ CREATE INDEX "index v2" ON "statutarni_organ_relation" (
	"statutarni_organ_id",
	"company_id",
	"id"
); """

    zapis2 = """ CREATE INDEX "index zapis2" ON "zapis_soudy" (
	"company_id"
); """

    zapis_soudy = """ CREATE INDEX "index zapis_soudy" ON "zapis_soudy" (
	"id",
	"company_id",
	"zapis_datum",
	"vymaz_datum",
	"oddil",
	"vlozka",
	"soud"
); """

    zpusob_jednani = """ CREATE INDEX "index zpusob_jednani" ON "zpusoby_jednani" (
	"id",
	"zpusob_jednani_text"
); """

    zpusob_jednani_relation = """ CREATE INDEX "index zpusob_jednani_relation" ON "zpusoby_jednani_relation" (
	"id",
	"statutarni_organ_id",
	"zpusob_jednani_id",
	"zapis_datum",
	"vymaz_datum"
); """

    zpusoby_jednani = """ CREATE INDEX "index zpusoby_jednani" ON "zpusoby_jednani" (
	"zpusob_jednani_text"
); """

    pravnicke_osoby_index = """ CREATE INDEX "pravnicke_osoby_index" ON "pravnicke_osoby" (
	"ico",
	"reg_cislo",
	"nazev"
); """

    list_of_indices = [companies, adresy, adresa_text, akcie, akcionari, companies_ico, companies_nazvy, companies_vznik, dr_clen_relation, dr_relation, dr_relation2, insolvency_events, insolvency2, jmena_firem, nazvy_nazev_text, obce, obec_jmeno, osoby, ostatni_skutecnosti2, 
    pocty_clenu_organ, podily, podily_spolecnik, pravni_formy, predmety_cinnosti_relation_v2, predmety_podnikani_relation, predmety_cinnosti, predmety_podnikani, prokuriste, sidlo, sidlo_relation, sidlo2, soudni_zapis, spolecnici, spolecnici2, statutarni_organy, statutarni_organy_relation, 
    statutarni_organy_relation_v2, v2, zapis2, zapis_soudy, zpusob_jednani, zpusob_jednani_relation, zpusoby_jednani, pravnicke_osoby_index]
    for elem in list_of_indices:
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(e)






# purge_DB()
create_DB("justice_db.db")
# general_update("down")
# general_update("db_update")
# parse_to_DB("data/as-full-ceske_budejovice-2021.xml")
# parse_to_DB("data/sro-full-ceske_budejovice-2021.xml")

# parse_to_DB("sro-actual-praha-2020.xml")




# do_both()

cProfile.run('general_update("db_update")')