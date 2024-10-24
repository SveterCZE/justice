from datetime import datetime
import os
from lxml import etree
from sqlalchemy import insert
import inspect

# import sqlite3
# from app import cur

# The function opens a file and parses the extracted data into the database
def update_DB(file, conn):
    print("Processing ", str(file))
    # conn = sqlite3.connect(DB_name)
    c = conn.cursor()
    for event, element in etree.iterparse(file, tag="Subjekt"):
        # Bugfix for companies which have been deleted but appear in the list of existing companies
        if ([element.find('vymazDatum')][0]) != None:
            continue
        else:
            ICO = get_ICO(element)
            # Bugfix to skip the old companies that have no Identification No.
            if ICO == False:
                continue
            # Vlozit prazdny radek s ICO
            insert_new_ICO(c, ICO, element)
            # print(ICO)
            primary_sql_key = get_primary_sql_key(c, ICO)
            # Vlozit jednolive parametry
            find_other_properties(c, ICO, element, conn, primary_sql_key)
            element.clear()
    conn.commit()
    # conn.close()
    return 0

def get_ICO(element):
    ico = element.find('ico')
    if ico == None:
        return False
    else:
        return element.find('ico').text

# Function to attempt to insert a placeholder for a new company based on ICO
def insert_new_ICO(c, ICO, element):
    try:
        datum_zapis = get_prop(element, "zapisDatum")
        nazev = get_prop(element, "nazev")
        c.execute("INSERT INTO companies (ico, zapis, nazev) VALUES (%s, %s, %s);", (ICO, datum_zapis, nazev,))
        return c.lastrowid
    except Exception as e:
        print(e)

def get_primary_sql_key(c, ICO):
    try:
        primary_key = c.execute("SELECT id FROM companies WHERE ico = (%s)", (ICO,))
        primary_key = c.fetchone()
        if primary_key == None:
            return False
        else:
            return primary_key[0]
    except Exception as e:
        print(e)
        return 0

def insert_company_relations(c, element, primary_sql_key):
    insert_instructions = [(".//udaje/Udaj/pravniForma/nazev", "pravni_formy", "pravni_forma", "pravni_formy_relation")]
    for elem in insert_instructions:
        insert_individual_relations(c, element, primary_sql_key, elem)
    return 0

def insert_individual_relations(c, element, primary_sql_key, elem):
    inserted_figure = str(get_prop(element, elem[0]))
    insert_into_ancillary_table(c, elem, inserted_figure)
    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
    insert_relation_information(c, elem, primary_sql_key, ancillary_table_key)
    return ancillary_table_key

def insert_relation_information(c, elem, primary_sql_key, ancillary_table_key):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(%s, %s)", (primary_sql_key, ancillary_table_key,))
    except Exception as e:
        print(e)
    return 0


def find_other_properties(c, ICO, element, conn, primary_sql_key):
    try:
        my_iter = element.findall("udaje")
        for elem in my_iter:
            my_iter2 = elem.findall("Udaj")
            for elem2 in my_iter2:
                udajTyp_name = get_prop(elem2, ".//udajTyp/kod")
                if udajTyp_name == "SIDLO":
                    find_registered_office(c, elem2, primary_sql_key)
                elif udajTyp_name == "NAZEV":
                    find_nazev(c, elem2, primary_sql_key)
                elif udajTyp_name == "SPIS_ZN":
                    find_sp_zn(c, elem2, primary_sql_key)
                elif udajTyp_name == "PRAVNI_FORMA":
                    find_pravni_forma(c, elem2, primary_sql_key)
                elif udajTyp_name == "STATUTARNI_ORGAN":
                    find_statutar(c, elem2, primary_sql_key)
                elif udajTyp_name == "SPOLECNIK":
                    find_spolecnik(c, elem2, primary_sql_key)
                elif udajTyp_name == "PREDMET_PODNIKANI_SEKCE":
                    find_predmet_podnikani(c, elem2, primary_sql_key)
                elif udajTyp_name == "PREDMET_CINNOSTI_SEKCE":
                    find_predmet_cinnosti(c, elem2, primary_sql_key)
                elif udajTyp_name == "UCEL_SUBJEKTU_SEKCE":
                    find_ucel(c, elem2, primary_sql_key)
                elif udajTyp_name == "ZAKLADNI_KAPITAL":
                    find_zakladni_kapital(c, elem2, primary_sql_key)
                elif udajTyp_name == "OST_SKUTECNOSTI_SEKCE":
                    find_ostatni_skutecnosti(c, elem2, primary_sql_key)
                elif udajTyp_name == "AKCIE_SEKCE":
                    find_akcie(c, elem2, primary_sql_key)
                elif udajTyp_name == "DOZORCI_RADA":
                    find_dozorci_rada(c, elem2, primary_sql_key)
                elif udajTyp_name == "PROKURA":
                    find_prokura(c, elem2, primary_sql_key)
                elif udajTyp_name == "AKCIONAR_SEKCE":
                    find_sole_shareholder(c, elem2, primary_sql_key)
                elif udajTyp_name == "INSOLVENCE_SEKCE":
                    find_insolvency(c, elem2, primary_sql_key)
                elif udajTyp_name == "KONKURS_SEKCE":
                    find_konkurz(c, elem2, primary_sql_key)
                elif udajTyp_name == "SKUTECNY_MAJITEL_SEKCE":
                    find_UBO(c, elem2, primary_sql_key)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_registered_office(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, ".//zapisDatum")
        vymaz_datum = get_prop(elem2, ".//vymazDatum")
        sidlo_id = find_sidlo(c, elem2)
        insert_instructions = [None,"adresy", "adresa_text", "sidlo_relation"]
        insert_relation_information_v2(c, insert_instructions, primary_sql_key, sidlo_id, zapis_datum, vymaz_datum)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_nazev(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, ".//zapisDatum")
        vymaz_datum = get_prop(elem2, ".//vymazDatum")
        nazev = get_prop(elem2, ".//hodnotaText")
        sql = """INSERT INTO nazvy (company_id, zapis_datum, vymaz_datum, nazev_text) VALUES(%s, %s, %s, %s)"""
        c.execute(sql, (primary_sql_key, zapis_datum, vymaz_datum, nazev,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_sp_zn(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, ".//zapisDatum")
        vymaz_datum = get_prop(elem2, ".//vymazDatum")
        soud = get_prop(elem2, ".//spisZn/soud/kod")
        oddil = get_prop(elem2, ".//spisZn/oddil")
        vlozka = get_prop(elem2, ".//spisZn/vlozka")
        sql = """INSERT INTO zapis_soudy (company_id, zapis_datum, vymaz_datum, oddil, vlozka, soud) VALUES(%s, %s, %s, %s, %s, %s)"""
        c.execute(sql, (primary_sql_key, zapis_datum, vymaz_datum, oddil, vlozka, soud))
        if vymaz_datum == None:
             c.execute("UPDATE companies SET oddil = (%s), vlozka = (%s), soud = (%s) WHERE id = (%s)",(oddil,vlozka,soud,primary_sql_key,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_pravni_forma(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, ".//zapisDatum")
        vymaz_datum = get_prop(elem2, ".//vymazDatum")
        pravni_forma = get_prop(elem2, ".//pravniForma/nazev")
        insert_instructions = [(pravni_forma,"pravni_formy", "pravni_forma", "pravni_formy_relation")]
        for elem in insert_instructions:
            ancillary_table_key = get_anciallary_table_key(c, elem, pravni_forma)
            if ancillary_table_key == False:
                insert_into_ancillary_table(c, elem, pravni_forma)
                ancillary_table_key = get_anciallary_table_key(c, elem, pravni_forma)
            insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_statutar(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, "zapisDatum")
        vymaz_datum = get_prop(elem2, "vymazDatum")
        oznaceni_statutar_organu = get_prop(elem2, ".//hlavicka")
        insert_instructions = [(oznaceni_statutar_organu,"statutarni_organy", "statutarni_organ_text", "statutarni_organ_relation")]
        for elem in insert_instructions:
            ancillary_table_key = get_anciallary_table_key(c, elem, oznaceni_statutar_organu)
            if ancillary_table_key == False:
                insert_into_ancillary_table(c, elem, oznaceni_statutar_organu)
            ancillary_table_key = get_anciallary_table_key(c, elem, oznaceni_statutar_organu)
            insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
            relationship_table_key = get_relationship_table_key(c, primary_sql_key, ancillary_table_key)
        my_iter = elem2.findall("podudaje/Udaj") 
        for elem in my_iter:
            udajTyp_name = get_prop(elem, "udajTyp/kod")
            if udajTyp_name == "POCET_CLENU":
                find_pocet_clenu(c, elem, relationship_table_key)
            elif udajTyp_name == "ZPUSOB_JEDNANI":
                find_zpusob_jednani(c, elem, relationship_table_key)
            elif udajTyp_name == "STATUTARNI_ORGAN_CLEN":
                find_clen_statut_org(c, elem, relationship_table_key)
            else:
                pass
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_UBO(c, elem2, primary_sql_key):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            zapis_datum = get_prop(elem, "zapisDatum")
            vymaz_datum = get_prop(elem, "vymazDatum")
            postaveni = get_prop(elem, "hodnotaUdaje/postaveni").split(";")[0]
            koncovyPrijemceText = get_prop(elem, "hodnotaUdaje/koncovyPrijemceText")
            skutecnymMajitelemOd = get_prop(elem, "hodnotaUdaje/skutecnymMajitelemOd")
            vlastniPodilNaProspechu = get_prop(elem, "hodnotaUdaje/vlastniPodilNaProspechu")
            vlastniPodilNaProspechu_typ = get_prop(elem, "hodnotaUdaje/podilNaProspechu/typ")
            vlastniPodilNaProspechu_textValue = get_prop(elem, "hodnotaUdaje/podilNaProspechu/textValue")
            vlastniPodilNaHlasovani = get_prop(elem, "hodnotaUdaje/podilNaHlasovani")
            vlastniPodilNaHlasovani_typ = get_prop(elem, "hodnotaUdaje/podilNaHlasovani/typ")
            vlastniPodilNaHlasovani_value = get_prop(elem, "hodnotaUdaje/podilNaHlasovani/textValue")
            adresa_id = find_sidlo(c, elem)
            UBO_id = find_fyzicka_osoba(c, elem, adresa_id)
            c.execute("INSERT INTO ubo (company_id, ubo_id, adresa_id, zapis_datum, vymaz_datum, postaveni, koncovy_prijemce_text, skutecnym_majitelem_od, vlastni_podil_na_prospechu, vlastni_podil_na_prospechu_typ, vlastni_podil_na_prospechu_text_value, vlastni_podil_na_hlasovani, vlastni_podil_na_hlasovani_typ, vlastni_podil_na_hlasovani_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                      (primary_sql_key, UBO_id, adresa_id, zapis_datum, vymaz_datum, postaveni, koncovyPrijemceText, skutecnymMajitelemOd, vlastniPodilNaProspechu, vlastniPodilNaProspechu_typ, vlastniPodilNaProspechu_textValue, vlastniPodilNaHlasovani, vlastniPodilNaHlasovani_typ, vlastniPodilNaHlasovani_value,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_spolecnik(c, elem2, primary_sql_key):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            spolecnik_kod = get_prop(elem, "udajTyp/kod")
            zapis_datum = get_prop(elem, "zapisDatum")
            vymaz_datum = get_prop(elem, "vymazDatum")
            spolecnik_typ =  get_prop(elem, "hodnotaUdaje/typ")
            if spolecnik_kod == "SPOLECNIK_OSOBA" and spolecnik_typ == "OSOBA":
                text_spolecnik = get_prop(elem, "hodnotaUdaje/textZaOsobu/value")
                nazev = get_prop(elem, "osoba/nazev")
                if nazev == None:
                    adresa_id = find_sidlo(c, elem)
                    spolecnik_fo_id = find_fyzicka_osoba(c, elem, adresa_id)
                    c.execute("INSERT INTO spolecnici (company_id, spolecnik_fo_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", (primary_sql_key, spolecnik_fo_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik,))
                    # c.execute ("SELECT last_insert_rowid()")
                    spolecnik_id = c.fetchone()[0]
                else:
                    spol_ico = get_prop(elem, "osoba/ico")
                    regCislo = get_prop(elem, "osoba/regCislo")
                    adresa_id = find_sidlo(c, elem)
                    spolecnik_po_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
                    c.execute("INSERT INTO spolecnici (company_id, spolecnik_po_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", (primary_sql_key, spolecnik_po_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik,))
                    # c.execute ("SELECT last_insert_rowid()")
                    spolecnik_id = c.fetchone()[0]
                insert_podily(c, elem, spolecnik_id)
            
            elif spolecnik_kod == "SPOLECNIK_OSOBA" and spolecnik_typ == "SPOLECNY_PODIL":
                text_spolecny_podil = get_prop(elem, "hodnotaUdaje/textZaOsobu/value")
                c.execute("INSERT INTO spolecnici_spolecny_podil (company_id, zapis_datum, vymaz_datum, text_spolecny_podil) VALUES (%s, %s, %s, %s) RETURNING id", (primary_sql_key, zapis_datum, vymaz_datum, text_spolecny_podil,))               
                # c.execute ("SELECT last_insert_rowid()")
                spolecny_op_id = c.fetchone()[0]               
                insert_common_podily(c, elem, spolecny_op_id)
                insert_common_shareholders(c, elem, spolecny_op_id)

            elif spolecnik_kod == "SPOLECNIK_OSOBA" and spolecnik_typ == "UVOLNENY_PODIL":
                text_uvolneny_podil = get_prop(elem, "hodnotaUdaje/textZaOsobu/value")
                c.execute("INSERT INTO spolecnici_uvolneny_podil (company_id, zapis_datum, vymaz_datum, text_uvolneny_podil) VALUES (%s, %s, %s, %s) RETURNING id", (primary_sql_key, zapis_datum, vymaz_datum, text_uvolneny_podil,))               
                # c.execute ("SELECT last_insert_rowid()")
                uvolneny_op_id = c.fetchone()[0]
                insert_vacant_podily(c, elem, uvolneny_op_id)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def insert_common_shareholders(c, elem, spolecny_op_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            if str(get_prop(podil_elem, "udajTyp/kod")) == "SPOLECNIK_PODILNIK":
                zapisDatum = get_prop(podil_elem, "zapisDatum")
                vymazDatum = get_prop(podil_elem, "vymazDatum")
                typ_podilnika = get_prop(podil_elem, "hodnotaText")
                if typ_podilnika == "AngazmaFyzicke":
                    adresa_id = find_sidlo(c, podil_elem)
                    spolecnik_fo_id = find_fyzicka_osoba(c, podil_elem, adresa_id)
                    c.execute("INSERT INTO podilnici (podil_id, podilnik_fo_id, zapis_datum, vymaz_datum, adresa_id) VALUES (%s, %s, %s, %s, %s)", (spolecny_op_id, spolecnik_fo_id, zapisDatum, vymazDatum, adresa_id))
                if typ_podilnika == "AngazmaPravnicke":
                    spol_ico = get_prop(podil_elem, "osoba/ico")
                    regCislo = get_prop(podil_elem, "osoba/regCislo")
                    adresa_id = find_sidlo(c, podil_elem)
                    spolecnik_po_id = find_pravnicka_osoba(c, podil_elem, spol_ico, regCislo, adresa_id)
                    c.execute("INSERT INTO podilnici (podil_id, podilnik_po_id, zapis_datum, vymaz_datum, adresa_id) VALUES (%s, %s, %s, %s, %s)", (spolecny_op_id, spolecnik_po_id, zapisDatum, vymazDatum, adresa_id))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_predmet_podnikani(c, predmet_podnikani_elem, primary_sql_key):
    try:
        my_iter = predmet_podnikani_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = get_prop(elem2, ".//zapisDatum")
                vymaz_datum = get_prop(elem2, ".//vymazDatum")
                insert_instructions = [(".//hodnotaText","predmety_podnikani", "predmet_podnikani", "predmety_podnikani_relation")]
                for elem in insert_instructions:
                    inserted_figure = get_prop(elem2, ".//hodnotaText")
                    if inserted_figure != None:
                        inserted_figure = inserted_figure.capitalize()
                        if len(inserted_figure) > 2700:
                            inserted_figure = inserted_figure[:2700]
                        ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                        if ancillary_table_key == False:
                            insert_into_ancillary_table(c, elem, inserted_figure)
                            ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                        insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_predmet_cinnosti(c, predmet_cinnosti_elem, primary_sql_key):
    try:
        my_iter = predmet_cinnosti_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = get_prop(elem2, ".//zapisDatum")
                vymaz_datum = get_prop(elem2, ".//vymazDatum")
                insert_instructions = [(".//hodnotaText","predmety_cinnosti", "predmet_cinnosti", "predmety_cinnosti_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText"))
                    if inserted_figure != None:
                        inserted_figure = inserted_figure.capitalize()
                        if len(inserted_figure) > 2700:
                            inserted_figure = inserted_figure[:2700]
                        ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                        if ancillary_table_key == False:
                            insert_into_ancillary_table(c, elem, inserted_figure)
                            ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                        insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_ucel(c, ucel_elem, primary_sql_key):
    try:
        my_iter = ucel_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = get_prop(elem2, ".//zapisDatum")
                vymaz_datum = get_prop(elem2, ".//vymazDatum")
                insert_instructions = [(".//hodnotaText", "ucel", "ucel", "ucel_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText"))
                    if inserted_figure != None:
                        inserted_figure = inserted_figure.capitalize()
                        if len(inserted_figure) > 2700:
                            inserted_figure = inserted_figure[:2700]
                        ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                        if ancillary_table_key == False:
                            insert_into_ancillary_table(c, elem, inserted_figure)
                            ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                        insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_zakladni_kapital(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, ".//zapisDatum")
        vymaz_datum = get_prop(elem2, ".//vymazDatum")
        vklad_typ = get_prop(elem2, ".//hodnotaUdaje/vklad/typ")
        vklad_hodnota = get_prop(elem2, ".//hodnotaUdaje/vklad/textValue")
        splaceni_typ = get_prop(elem2, ".//hodnotaUdaje/splaceni/typ")
        splaceni_hodnota = get_prop(elem2, ".//hodnotaUdaje/splaceni/textValue")
        c.execute("INSERT INTO zakladni_kapital (company_id, zapis_datum, vymaz_datum, vklad_typ, vklad_hodnota, splaceni_typ, splaceni_hodnota) VALUES(%s, %s, %s, %s, %s, %s, %s)", (primary_sql_key, zapis_datum, vymaz_datum, vklad_typ, vklad_hodnota, splaceni_typ, splaceni_hodnota,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_ostatni_skutecnosti(c, ostatni_skutecnosti_elem, primary_sql_key):
    try:
        my_iter = ostatni_skutecnosti_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = get_prop(elem2, ".//zapisDatum")
                vymaz_datum = get_prop(elem2, ".//vymazDatum")
                inserted_figure = get_prop(elem2, ".//hodnotaText")
                c.execute("INSERT INTO ostatni_skutecnosti (company_id, zapis_datum, vymaz_datum, ostatni_skutecnost) VALUES(%s, %s, %s, %s)", (primary_sql_key, zapis_datum, vymaz_datum, inserted_figure,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_akcie(c, ostatni_akcie_elem, primary_sql_key):
    try:
        my_iter = ostatni_akcie_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = get_prop(elem2, ".//zapisDatum")
                vymaz_datum = get_prop(elem2, ".//vymazDatum")
                akcie_podoba = get_prop(elem2, ".//hodnotaUdaje/podoba")
                akcie_typ = get_prop(elem2, ".//hodnotaUdaje/typ")
                akcie_pocet = get_prop(elem2, ".//hodnotaUdaje/pocet")
                akcie_hodnota_typ = get_prop(elem2, ".//hodnotaUdaje/hodnota/typ")
                akcie_hodnota_value = get_prop(elem2, ".//hodnotaUdaje/hodnota/textValue")
                akcie_text = get_prop(elem2, ".//hodnotaUdaje/text")
                c.execute("INSERT INTO akcie (company_id, zapis_datum, vymaz_datum, akcie_podoba, akcie_typ, akcie_pocet, akcie_hodnota_typ, akcie_hodnota_value, akcie_text) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                          (primary_sql_key, zapis_datum, vymaz_datum, akcie_podoba, akcie_typ, akcie_pocet, akcie_hodnota_typ, akcie_hodnota_value,akcie_text,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   

def find_dozorci_rada(c, elem2, primary_sql_key):
    try:
        zapis_datum = get_prop(elem2, "zapisDatum")
        vymaz_datum = get_prop(elem2, "vymazDatum")
        c.execute("INSERT into dozorci_rada_relation (company_id, zapis_datum, vymaz_datum) VALUES (%s, %s, %s) RETURNING id", (primary_sql_key, zapis_datum, vymaz_datum,))
        # c.execute("SELECT id FROM dozorci_rada_relation WHERE company_id = (%s) and zapis_datum = (%s)", (primary_sql_key,zapis_datum,))
        relationship_table_key = c.fetchone()[0]
        my_iter = elem2.findall("podudaje/Udaj") 
        for elem in my_iter:
            udajTyp_name = get_prop(elem, "udajTyp/kod")
            if udajTyp_name == "POCET_CLENU_DOZORCI_RADA":
                find_pocet_clenu_dr(c, elem, relationship_table_key)
            elif udajTyp_name == "DOZORCI_RADA_CLEN":
                find_clen_dr(c, elem, relationship_table_key)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)      

def find_prokura(c, elem2, primary_sql_key):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            typ_zapis = get_prop(elem, "udajTyp/kod")
            if typ_zapis == "PROKURA_OSOBA":
                zapis_datum = get_prop(elem, "zapisDatum")
                vymaz_datum = get_prop(elem, "vymazDatum")
                text_prokurista = get_prop(elem, "hodnotaUdaje/textZaOsobu/value")
                adresa_id = find_sidlo(c, elem)
                prokurista_fo_id = find_fyzicka_osoba(c, elem, adresa_id)
                c.execute("INSERT INTO prokuriste (company_id, zapis_datum, vymaz_datum, prokurista_fo_id, adresa_id, text_prokurista) VALUES (%s, %s, %s, %s, %s, %s)", (primary_sql_key, zapis_datum, vymaz_datum, prokurista_fo_id, adresa_id, text_prokurista,))
            else:
                zapis_datum = get_prop(elem, "zapisDatum")
                vymaz_datum = get_prop(elem, "vymazDatum")
                prokura_text = get_prop(elem, "hodnotaText")
                c.execute("INSERT INTO prokura_common_texts (company_id, zapis_datum, vymaz_datum, prokura_text) VALUES (%s, %s, %s, %s)", (primary_sql_key, zapis_datum, vymaz_datum, prokura_text,)) 
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_sole_shareholder(c, elem2, primary_sql_key):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            zapis_datum = get_prop(elem, "zapisDatum")
            vymaz_datum = get_prop(elem, "vymazDatum")
            text_akcionar = get_prop(elem, "hodnotaUdaje/textZaOsobu/value")
            typ_akcionar = get_prop(elem, "hodnotaUdaje/T")
            if typ_akcionar == "P":
                spol_ico = get_prop(elem, "osoba/ico")
                regCislo = get_prop(elem, "osoba/regCislo")
                adresa_id = find_sidlo(c, elem)
                akcionar_po_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
                c.execute("INSERT into jediny_akcionar (company_id, zapis_datum, vymaz_datum, text_akcionar, akcionar_po_id, adresa_id) VALUES (%s, %s, %s, %s, %s, %s)", (primary_sql_key, zapis_datum, vymaz_datum, text_akcionar, akcionar_po_id, adresa_id,))
            elif typ_akcionar == "F":
                adresa_id = find_sidlo(c, elem)
                akcionar_fo_id = find_fyzicka_osoba(c, elem, adresa_id)
                c.execute("INSERT into jediny_akcionar (company_id, zapis_datum, vymaz_datum, text_akcionar, akcionar_fo_id, adresa_id) VALUES (%s, %s, %s, %s, %s, %s)", (primary_sql_key, zapis_datum, vymaz_datum, text_akcionar, akcionar_fo_id, adresa_id,))    
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_insolvency(c, insolvency_elem, primary_sql_key):
   try:
       my_iter = insolvency_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
                    insolvency_text = get_prop(elem2, ".//text")
                    zapis_datum = get_prop(elem2, ".//zapisDatum")
                    vymaz_datum = get_prop(elem2, ".//vymazDatum")
                    if insolvency_text != None:
                        try:
                            sql_search = "SELECT * FROM insolvency_events WHERE company_id = %s and insolvency_event = %s"
                            c.execute(sql_search, (primary_sql_key, insolvency_text,))
                            record_id = c.fetchone()
                            if record_id == None:
                                sql_insert = "INSERT INTO insolvency_events (company_id, zapis_datum, vymaz_datum, insolvency_event) VALUES(%s, %s, %s, %s)"
                                c.execute(sql_insert, (primary_sql_key, zapis_datum, vymaz_datum, insolvency_text,))
                        except Exception as f:
                            print(inspect.stack()[0][3])
                            print(f)
   except Exception as x:
       print(inspect.stack()[0][3])
       print(x)

def find_konkurz(c, konkurz_elem, primary_sql_key):
    try:
       my_iter = konkurz_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
                    konkurz_text = get_prop(elem2, ".//text")
                    zapis_datum = get_prop(elem2, ".//zapisDatum")
                    vymaz_datum = get_prop(elem2, ".//vymazDatum")
                    if konkurz_text != None:
                        try:
                            sql_insert = "INSERT INTO konkurz_events (company_id, zapis_datum, vymaz_datum, konkurz_event) VALUES(%s, %s, %s, %s)"
                            c.execute(sql_insert, (primary_sql_key, zapis_datum, vymaz_datum, konkurz_text,))
                        except Exception as f:
                            print(inspect.stack()[0][3])
                            print(f)   
    except Exception as x:
        print(inspect.stack()[0][3])
        print(x)   

def find_sidlo(c, elem):
    try:
        statNazev = get_prop(elem, ".//statNazev")
        obec = get_prop(elem, ".//obec")
        ulice = get_prop(elem, ".//ulice")
        if ulice != None and ('\'' in ulice or '"' in ulice):
            ulice = ulice.replace('\'', '')
        castObce = get_prop(elem, ".//castObce")
        cisloPo = get_prop(elem, ".//cisloPo")
        cisloOr = get_prop(elem, ".//cisloOr")
        psc = get_prop(elem, ".//psc")
        okres = get_prop(elem, ".//okres")
        adresaText = get_prop(elem, ".//adresaText")
        if adresaText != None and ('\'' in adresaText):
            adresaText = adresaText.replace('\'', '')
        cisloEv = get_prop(elem, ".//cisloEv")
        cisloText = get_prop(elem, ".//cisloText")
        
        insert_address(c, statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText)
        adresa_id = c.fetchone()[0]
        
        # adresa_id = find_address_id(c, statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText)
        # if adresa_id == False:
        #     insert_address(c, statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText)
        #     adresa_id = c.fetchone()[0]
            # if adresa_id == False:
            #     print(statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText)
        return adresa_id
    except Exception as e:
        print(inspect.stack()[0][3])
        print(e)

# def find_address_id(c, stat, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, komplet_adresa, cisloEv, cisloText):
#     try:
#         sql_query = ["SELECT id FROM adresy_v2 WHERE "]
#         iterable_variables = [(k, v) for k, v in locals().items()]
#         initial_element_inserted = False
#         for elem in iterable_variables:
#             if elem[0] == "c" or elem[0] == "sql_query":
#                 pass
#             elif elem[1] == None:
#                 if initial_element_inserted == True:
#                     sql_query.append(" and ")
#                 sql_query.append(f"{elem[0]} IS NULL")
#                 initial_element_inserted = True
#             else:
#                 if initial_element_inserted == True:
#                     sql_query.append(" and ")
#                 sql_query.append(f"{elem[0]} = '{elem[1]}'")
#                 initial_element_inserted = True
#         sql_query = " ".join(sql_query)
#         adresa_id = c.execute(sql_query)
#         if adresa_id == None:
#             return False
#         adresa_id = c.fetchone()[0]
#         return adresa_id
#     except Exception as f:
#         return False 

def insert_address(c, statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText):
    try:
        c.execute("INSERT INTO adresy_v2 (stat, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, komplet_adresa, cisloEv, cisloText) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT not_distinct_address DO UPDATE SET obec=EXCLUDED.obec RETURNING id", (statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)


def insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(DEFAULT, %s, %s, %s, %s)", (primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def insert_into_ancillary_table(c, elem, inserted_figure):
    try:
        c.execute("INSERT INTO " + elem[1] + "(" + elem[2] + ") VALUES(%s)", (inserted_figure,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def get_anciallary_table_key(c, elem, inserted_figure):
    try:
        c.execute("SELECT id FROM " + elem[1] + " WHERE " + elem[2] + " = (%s)", (inserted_figure,))
        anciallary_table_key = c.fetchone()
        if anciallary_table_key == None:
            return False
        else:
            return anciallary_table_key[0]
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def get_relationship_table_key(c, primary_sql_key, ancillary_table_key):
    c.execute("SELECT id FROM statutarni_organ_relation WHERE company_id = (%s) and statutarni_organ_id = (%s)", (primary_sql_key,ancillary_table_key,))
    return c.fetchone()[0]

def find_pocet_clenu(c, elem, relationship_table_key):
    try:
        zapis_datum = get_prop(elem, "zapisDatum")
        vymaz_datum = get_prop(elem, "vymazDatum")
        pocet_clenu_number = get_prop(elem, "hodnotaText")
        c.execute("INSERT into pocty_clenu_organu (organ_id, pocet_clenu_value, zapis_datum, vymaz_datum) VALUES (%s,%s,%s,%s)", (relationship_table_key, pocet_clenu_number, zapis_datum, vymaz_datum))        
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_zpusob_jednani(c, elem, relationship_table_key):
    try:
        zapis_datum = get_prop(elem, "zapisDatum")
        vymaz_datum = get_prop(elem, "vymazDatum")
        zpusob_jednani = get_prop(elem, "hodnotaText")
        if zpusob_jednani != None and len(zpusob_jednani) > 2700:
            zpusob_jednani = zpusob_jednani[:2700]
        insert_instructions = [(zpusob_jednani,"zpusoby_jednani", "zpusob_jednani_text", "zpusoby_jednani_relation")]
        for elem in insert_instructions:
            ancillary_table_key = get_anciallary_table_key(c, elem, zpusob_jednani)
            if ancillary_table_key == False:
                insert_into_ancillary_table(c, elem, zpusob_jednani)
                ancillary_table_key = get_anciallary_table_key(c, elem, zpusob_jednani)
            if ancillary_table_key != False:
                insert_relation_information_v2(c, elem, relationship_table_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_clen_statut_org(c, elem, relationship_table_key):
    try:
        zapis_datum = get_prop(elem, "zapisDatum")
        vymaz_datum = get_prop(elem, "vymazDatum")
        funkce_statutar_organu = get_prop(elem, "funkce")
        typ_osoby = get_prop(elem, "hodnotaText")
        funkceOd = get_prop(elem, "funkceOd")
        clenstviOd = get_prop(elem, "clenstviOd")
        funkceDo = get_prop(elem, "funkceDo")
        clenstviDo = get_prop(elem, "clenstviDo")
        if typ_osoby == "AngazmaFyzicke":
            adresa_id = find_sidlo(c, elem)
            osoba_id = find_fyzicka_osoba(c, elem, adresa_id)
            c.execute("INSERT into statutarni_organ_clen_relation (statutarni_organ_id, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                      (relationship_table_key, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
        if typ_osoby == "AngazmaPravnicke":
            spol_ico = get_prop(elem, "osoba/ico")
            regCislo = get_prop(elem, "osoba/regCislo")
            adresa_id = find_sidlo(c, elem)
            prav_osoba_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
            c.execute("INSERT into statutarni_organ_clen_relation (statutarni_organ_id, prav_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                      (relationship_table_key, prav_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_fyzicka_osoba(c, elem, adresa_id):
    try:
        jmeno = lower_names_chars(get_prop(elem, "osoba/jmeno"))
        prijmeni = lower_names_chars(get_prop(elem, "osoba/prijmeni"))
        if jmeno == None and prijmeni == None:
            prijmeni = lower_names_chars(get_prop(elem, "osoba/osobaText"))
        if jmeno != None and ('\'' in jmeno):
            jmeno = jmeno.replace('\'', '')
        if prijmeni != None and ('\'' in prijmeni):
            prijmeni = prijmeni.replace('\'', '')  
        datum_narozeni = get_prop(elem, "osoba/narozDatum")
        titulPred = get_prop(elem, "osoba/titulPred")
        titulZa = get_prop(elem, "osoba/titulZa")
        insert_fyzicka_osoba(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id)
        osoba_id = c.fetchone()[0]
        # osoba_id = find_osoba_id(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id)
        # if osoba_id == False:
        #     insert_fyzicka_osoba(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id)
        #     osoba_id = c.fetchone()[0]
        return osoba_id
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)
        pass

def lower_names_chars(string_name):
    if string_name == None:
        return None
    else:
        updated_name = ""
        previous_non_alpha = True
        for elem in string_name:
            if previous_non_alpha == True:
                updated_name += elem
            else:
                updated_name += elem.lower()
            if elem.isalpha() == True:
                previous_non_alpha = False
            else:
                previous_non_alpha = True
        return updated_name

def insert_fyzicka_osoba(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id):
    try:
        c.execute("INSERT into fyzicke_osoby (titul_pred, jmeno, prijmeni, titul_za, datum_naroz, adresa_id) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT not_distinct_natural_person DO UPDATE SET adresa_id=EXCLUDED.adresa_id RETURNING id", (titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

# def find_osoba_id(c, titul_pred, jmeno, prijmeni, titul_za, datum_naroz, adresa_id):
#     try:
#         sql_query = "SELECT id FROM fyzicke_osoby WHERE ".split()
#         iterable_variables = [(k, v) for k, v in locals().items()]
#         for elem in iterable_variables:
#             if elem[0] == "c" or elem[0] == "sql_query" or elem[1] == None:
#                 pass
#             else:
#                 added_text = f"{elem[0]} = '{elem[1]}' and ".split()
#                 for part in added_text:
#                     sql_query.append(part)
#         sql_query = " ".join(sql_query[:-1])
#         anciallary_table_key = c.execute(sql_query)
#         anciallary_table_key = c.fetchone()[0]
#         return anciallary_table_key
#     except Exception as f:
#         return False 

def find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id):
    try:
        nazev = get_prop(elem, "osoba/nazev")
        if nazev != None and ('\'' in nazev in nazev):
            nazev = nazev.replace('\'', '')
        insert_pravnicka_osoba(c, spol_ico, regCislo, nazev, adresa_id)
        osoba_id = c.fetchone()[0]
        # osoba_id = find_pravnicka_osoba_id(c, spol_ico, regCislo, nazev, adresa_id)
        # if osoba_id == False:
        #     insert_pravnicka_osoba(c, spol_ico, regCislo, nazev, adresa_id)
        #     osoba_id = c.fetchone()[0]
        return osoba_id
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_pocet_clenu_dr(c, elem, relationship_table_key):
    try:
        zapis_datum = get_prop(elem, "zapisDatum")
        vymaz_datum = get_prop(elem, "vymazDatum")
        pocet_clenu_number = get_prop(elem, "hodnotaText")
        c.execute("INSERT into pocty_clenu_DR (organ_id, pocet_clenu_value, zapis_datum, vymaz_datum) VALUES (%s,%s,%s,%s)", (relationship_table_key, pocet_clenu_number, zapis_datum, vymaz_datum,))        
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def find_clen_dr(c, elem, relationship_table_key):
    try:
        zapis_datum = get_prop(elem, "zapisDatum")
        vymaz_datum = get_prop(elem, "vymazDatum")
        funkce_statutar_organu = get_prop(elem, "funkce")
        typ_osoby = get_prop(elem, "hodnotaText")
        funkceOd = get_prop(elem, "funkceOd")
        clenstviOd = get_prop(elem, "clenstviOd")
        funkceDo = get_prop(elem, "funkceDo")
        clenstviDo = get_prop(elem, "clenstviDo")
        if typ_osoby == "AngazmaFyzicke":
            adresa_id = find_sidlo(c, elem)
            osoba_id = find_fyzicka_osoba(c, elem, adresa_id)
            c.execute("INSERT into dr_organ_clen_relation (dozorci_rada_id, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                      (relationship_table_key, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
        elif typ_osoby == "AngazmaPravnicke":
            spol_ico = get_prop(elem, "osoba/ico")
            regCislo = get_prop(elem, "osoba/regCislo")
            adresa_id = find_sidlo(c, elem)
            pravnicka_osoba_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
            c.execute("INSERT into dr_organ_clen_relation (dozorci_rada_id, pravnicka_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                      (relationship_table_key, pravnicka_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

# TODO MERGE THESE THREE FUNCTIONS INTO ONE
def insert_podily(c, elem, spolecnik_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            zapisDatum = get_prop(podil_elem, "zapisDatum")
            vymazDatum = get_prop(podil_elem, "vymazDatum")
            druh_podilu_id = get_druh_podilu_id(c, podil_elem)
            vklad_typ = get_prop(podil_elem, "hodnotaUdaje/vklad/typ")
            vklad_text = get_prop(podil_elem, "hodnotaUdaje/vklad/textValue")
            souhrn_typ = get_prop(podil_elem, "hodnotaUdaje/souhrn/typ")
            souhrn_text = get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue")
            splaceni_typ = get_prop(podil_elem, "hodnotaUdaje/splaceni/typ")
            splaceni_text = get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue")
            c.execute("INSERT INTO podily (spolecnik_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id", (spolecnik_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
            podil_id = c.fetchone()[0]
            insert_pledge(c, podil_elem, podil_id)
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def insert_pledge(c, podil_elem, podil_id):
    try:
        pledge_iter = podil_elem.findall("podudaje/Udaj")
        for pledge_elem in pledge_iter:
            if str(get_prop(pledge_elem, "udajTyp/kod")) == "SPOLECNIK_ZASTAVNI_PRAVO":
                zapisDatum = get_prop(pledge_elem, "zapisDatum")
                vymazDatum = get_prop(pledge_elem, "vymazDatum")
                pledgeText = get_prop(pledge_elem, "hodnotaUdaje/text")
                c.execute("INSERT INTO zastavy (podil_id, zapis_datum, vymaz_datum, zastava_text) VALUES (%s,%s,%s,%s)", (podil_id, zapisDatum, vymazDatum, pledgeText,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)
        pass

def insert_vacant_podily(c, elem, vacant_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            zapisDatum = get_prop(podil_elem, "zapisDatum")
            vymazDatum = get_prop(podil_elem, "vymazDatum")
            druh_podilu_id = get_druh_podilu_id(c, podil_elem)
            vklad_typ = get_prop(podil_elem, "hodnotaUdaje/vklad/typ")
            vklad_text = get_prop(podil_elem, "hodnotaUdaje/vklad/textValue")
            souhrn_typ = get_prop(podil_elem, "hodnotaUdaje/souhrn/typ")
            souhrn_text = get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue")
            splaceni_typ = get_prop(podil_elem, "hodnotaUdaje/splaceni/typ")
            splaceni_text = get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue")
            c.execute("INSERT INTO podily (uvolneny_podil_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (vacant_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)    

def insert_common_podily(c, elem, common_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            if str(get_prop(podil_elem, "udajTyp/kod")) == "SPOLECNIK_PODIL":
                zapisDatum = get_prop(podil_elem, "zapisDatum")
                vymazDatum = get_prop(podil_elem, "vymazDatum")
                druh_podilu_id = get_druh_podilu_id(c, podil_elem)
                vklad_typ = get_prop(podil_elem, "hodnotaUdaje/vklad/typ")
                vklad_text = get_prop(podil_elem, "hodnotaUdaje/vklad/textValue")
                souhrn_typ = get_prop(podil_elem, "hodnotaUdaje/souhrn/typ")
                souhrn_text = get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue")
                splaceni_typ = get_prop(podil_elem, "hodnotaUdaje/splaceni/typ")
                splaceni_text = get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue")
                c.execute("INSERT INTO podily (spolecny_podil_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (common_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)   


def get_druh_podilu_id(c, podil_elem):
    try:
        druhPodilu = get_prop(podil_elem, "hodnotaUdaje/druhPodilu")
        if druhPodilu == None:
            druhPodilu = "N/A"
        druh_podilu_id = find_druh_podilu_id(c, druhPodilu)
        if druh_podilu_id == False:
            insert_druh_podilu(c, druhPodilu)
            druh_podilu_id = c.fetchone()[0]
        return druh_podilu_id
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f)

def insert_druh_podilu(c, druhPodilu):
    try:
        c.execute("INSERT INTO druhy_podilu (druh_podilu) VALUES (%s) RETURNING id", (druhPodilu,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f) 

def find_druh_podilu_id(c, druhPodilu):
    try:
        c.execute("SELECT id FROM druhy_podilu WHERE druh_podilu = (%s)", (druhPodilu,))
        druh_podilu_id = c.fetchone()
        if druh_podilu_id == None:
            return False
        else:
            return druh_podilu_id[0]
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f) 

# def find_pravnicka_osoba_id(c, ico, reg_cislo, nazev, adresa_id):
#     try:
#         sql_query = "SELECT id FROM pravnicke_osoby WHERE ".split()
#         iterable_variables = [(k, v) for k, v in locals().items()]
#         for elem in iterable_variables:
#             if elem[0] == "c" or elem[0] == "sql_query" or elem[1] == None:
#                 pass
#             else:
#                 added_text = f"{elem[0]} = '{elem[1]}' and ".split()
#                 for part in added_text:
#                     sql_query.append(part)
#         sql_query = " ".join(sql_query[:-1])
#         anciallary_table_key = c.execute(sql_query)
#         anciallary_table_key = c.fetchone()[0]
#         return anciallary_table_key
#     except Exception as f:
#         return False

def insert_pravnicka_osoba(c, spol_ico, regCislo, nazev, adresa_id):
    try:
        c.execute("INSERT into pravnicke_osoby (ico, reg_cislo, nazev, adresa_id) VALUES (%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT not_distinct_legal_person DO UPDATE SET adresa_id=EXCLUDED.adresa_id RETURNING id", (spol_ico, regCislo, nazev, adresa_id,))
    except Exception as f:
        print(inspect.stack()[0][3])
        print(f) 

def get_prop(element, prop):
    elem = element.find(prop)
    if elem == None:
        return None
    else:
        return str(elem.text)