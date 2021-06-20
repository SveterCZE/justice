from datetime import datetime
import os
from lxml import etree
import sqlite3

# The function opens a file and parses the extracted data into the database
def update_DB(file, DB_name):
    print("Processing ", str(file))
    conn = sqlite3.connect(DB_name)
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
            insert_company_relations(c, ICO, element, conn, primary_sql_key)
            find_other_properties(c, ICO, element, conn, primary_sql_key)
            element.clear()
    conn.commit()
    conn.close()
    return 0

def get_ICO(element):
    try:
        return element.find('ico').text
    except:
        return "00000000"

# Function to attempt to insert a placeholder for a new company based on ICO
def insert_new_ICO(c, ICO, conn, element):
    try:
        datum_zapis = str(get_prop(element, "zapisDatum"))
        nazev = str(get_prop(element, "nazev"))
        c.execute("INSERT INTO companies (ico, zapis, nazev) VALUES (?,?,?);", (ICO,datum_zapis,nazev,))
        return c.lastrowid
    except:
        pass

def get_primary_sql_key(c, ICO):
    try:
        primary_key = c.execute("SELECT id FROM companies WHERE ico = (?)", (ICO,))
        primary_key = c.fetchone()
        return primary_key[0]
    except:
        return 0

def insert_company_relations(c, ICO, element, conn, primary_sql_key):
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

def insert_relation_information(c, elem, primary_sql_key, ancillary_table_key):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(?, ?)", (primary_sql_key, ancillary_table_key,))
    except:
        pass
    return 0


def find_other_properties(c, ICO, element, conn, primary_sql_key):
    try:
        my_iter = element.findall("udaje")
        for elem in my_iter:
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
                elif udajTyp_name == "UCEL_SUBJEKTU_SEKCE":
                    find_ucel(c, ICO, elem2, conn, primary_sql_key, element)
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
                    find_insolvency(c, ICO, elem2, conn, primary_sql_key)
                elif udajTyp_name == "KONKURS_SEKCE":
                    find_konkurz(c, ICO, elem2, conn, primary_sql_key)
                elif udajTyp_name == "SKUTECNY_MAJITEL_SEKCE":
                    find_UBO(c, ICO, elem2, conn, primary_sql_key, element)

    except:
        pass

def find_registered_office(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        sidlo_id = find_sidlo(c, elem2, primary_sql_key)
        insert_instructions = [None,"adresy", "adresa_text", "sidlo_relation"]
        insert_relation_information_v2(c, insert_instructions, primary_sql_key, sidlo_id, zapis_datum, vymaz_datum)
    except Exception as f:
        print(f)   

def find_nazev(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        nazev = str(get_prop(elem2, ".//hodnotaText"))
        c.execute("INSERT INTO nazvy (company_id, zapis_datum, vymaz_datum, nazev_text) VALUES(?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, nazev,))
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

def find_pravni_forma(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
        vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
        pravni_forma = str(get_prop(elem2, ".//pravniForma/nazev"))
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
        insert_instructions = [(oznaceni_statutar_organu,"statutarni_organy", "statutarni_organ_text", "statutarni_organ_relation")]
        for elem in insert_instructions:
            insert_into_ancillary_table(c, elem, oznaceni_statutar_organu)
            ancillary_table_key = get_anciallary_table_key(c, elem, oznaceni_statutar_organu)
            insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
            relationship_table_key = get_relationship_table_key(c, primary_sql_key, ancillary_table_key)
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
                pass
    except Exception as f:
        print(f)

def find_UBO(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            zapis_datum = str(get_prop(elem, "zapisDatum"))
            vymaz_datum = str(get_prop(elem, "vymazDatum"))
            postaveni = str(get_prop(elem, "hodnotaUdaje/postaveni")).split(";")[0]
            koncovyPrijemceText = str(get_prop(elem, "hodnotaUdaje/koncovyPrijemceText"))
            skutecnymMajitelemOd = str(get_prop(elem, "hodnotaUdaje/skutecnymMajitelemOd"))
            vlastniPodilNaProspechu = str(get_prop(elem, "hodnotaUdaje/vlastniPodilNaProspechu"))
            vlastniPodilNaProspechu_typ = str(get_prop(elem, "hodnotaUdaje/podilNaProspechu/typ"))
            vlastniPodilNaProspechu_textValue = str(get_prop(elem, "hodnotaUdaje/podilNaProspechu/textValue"))
            vlastniPodilNaHlasovani = str(get_prop(elem, "hodnotaUdaje/podilNaHlasovani"))
            vlastniPodilNaHlasovani_typ = str(get_prop(elem, "hodnotaUdaje/podilNaHlasovani/typ"))
            vlastniPodilNaHlasovani_value = str(get_prop(elem, "hodnotaUdaje/podilNaHlasovani/textValue"))
            adresa_id = find_sidlo(c, elem, primary_sql_key)
            UBO_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element, adresa_id)
            c.execute("INSERT INTO ubo (company_id, UBO_id, adresa_id, zapis_datum, vymaz_datum, postaveni, koncovyPrijemceText, skutecnymMajitelemOd, vlastniPodilNaProspechu, vlastniPodilNaProspechu_typ, vlastniPodilNaProspechu_textValue, vlastniPodilNaHlasovani, vlastniPodilNaHlasovani_typ, vlastniPodilNaHlasovani_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (primary_sql_key, UBO_id, adresa_id, zapis_datum, vymaz_datum, postaveni, koncovyPrijemceText, skutecnymMajitelemOd, vlastniPodilNaProspechu, vlastniPodilNaProspechu_typ, vlastniPodilNaProspechu_textValue, vlastniPodilNaHlasovani, vlastniPodilNaHlasovani_typ, vlastniPodilNaHlasovani_value,))
    except Exception as f:
        print(f)

def find_spolecnik(c, ICO, elem2, conn, primary_sql_key, element):
    try:
        my_iter = elem2.findall("podudaje/Udaj")
        for elem in my_iter:
            spolecnik_kod = str(get_prop(elem, "udajTyp/kod"))
            zapis_datum = str(get_prop(elem, "zapisDatum"))
            vymaz_datum = str(get_prop(elem, "vymazDatum"))
            spolecnik_typ =  str(get_prop(elem, "hodnotaUdaje/typ"))
            # TODO Chech these conditions, they sometimes cause a person not being stored (IC 27650081)
            if spolecnik_kod == "SPOLECNIK_OSOBA" and spolecnik_typ == "OSOBA":
                # TODO alternativy pro None, Spolecny podil a Uvolneny podil
                text_spolecnik = str(get_prop(elem, "hodnotaUdaje/textZaOsobu/value"))
                nazev = str(get_prop(elem, "osoba/nazev"))
                # TODO Fix - make reference to type of person - some foreign persons have no ico or regCo, so they are assigned a number for a natural person
                if nazev == "0":
                    # I probably do not need the primary sql key
                    adresa_id = find_sidlo(c, elem, primary_sql_key)
                    spolecnik_fo_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element, adresa_id)
                    c.execute("INSERT INTO spolecnici (company_id, spolecnik_fo_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, spolecnik_fo_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik,))
                    c.execute ("SELECT last_insert_rowid()")
                    spolecnik_id = c.fetchone()[0]
                else:
                    spol_ico = str(get_prop(elem, "osoba/ico"))
                    regCislo = str(get_prop(elem, "osoba/regCislo"))
                    adresa_id = find_sidlo(c, elem, primary_sql_key)
                    spolecnik_po_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
                    c.execute("INSERT INTO spolecnici (company_id, spolecnik_po_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, spolecnik_po_id, zapis_datum, vymaz_datum, adresa_id, text_spolecnik,))
                    c.execute ("SELECT last_insert_rowid()")
                    spolecnik_id = c.fetchone()[0]
                insert_podily(c, elem, spolecnik_id)
            elif spolecnik_kod == "SPOLECNIK_OSOBA" and spolecnik_typ == "SPOLECNY_PODIL":
                text_spolecny_podil = str(get_prop(elem, "hodnotaUdaje/textZaOsobu/value"))
                c.execute("INSERT INTO spolecnici_spolecny_podil (company_id, zapis_datum, vymaz_datum, text_spolecny_podil) VALUES (?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, text_spolecny_podil,))               
                c.execute ("SELECT last_insert_rowid()")
                uvolneny_op_id = c.fetchone()[0]               
                insert_common_podily(c, elem, uvolneny_op_id)
            elif spolecnik_kod == "SPOLECNIK_OSOBA" and spolecnik_typ == "UVOLNENY_PODIL":
                text_uvolneny_podil = str(get_prop(elem, "hodnotaUdaje/textZaOsobu/value"))
                c.execute("INSERT INTO spolecnici_uvolneny_podil (company_id, zapis_datum, vymaz_datum, text_uvolneny_podil) VALUES (?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, text_uvolneny_podil,))               
                c.execute ("SELECT last_insert_rowid()")
                uvolneny_op_id = c.fetchone()[0]
                insert_vacant_podily(c, elem, uvolneny_op_id)
    except Exception as f:
        print(f)

def find_predmet_podnikani(c, ICO, predmet_podnikani_elem, conn, primary_sql_key, element):
    try:
        my_iter = predmet_podnikani_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                insert_instructions = [(".//hodnotaText","predmety_podnikani", "predmet_podnikani", "predmety_podnikani_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText")).capitalize()
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
                insert_instructions = [(".//hodnotaText","predmety_cinnosti", "predmet_cinnosti", "predmety_cinnosti_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText")).capitalize()
                    insert_into_ancillary_table(c, elem, inserted_figure)
                    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                    insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except:
        pass

def find_ucel(c, ICO, ucel_elem, conn, primary_sql_key, element):
    try:
        my_iter = ucel_elem.findall("podudaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                zapis_datum = str(get_prop(elem2, ".//zapisDatum"))
                vymaz_datum = str(get_prop(elem2, ".//vymazDatum"))
                insert_instructions = [(".//hodnotaText", "ucel", "ucel", "ucel_relation")]
                for elem in insert_instructions:
                    inserted_figure = str(get_prop(elem2, ".//hodnotaText")).capitalize()
                    insert_into_ancillary_table(c, elem, inserted_figure)
                    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
                    insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum)
    except Exception as f:
        print(f)


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
                adresa_id = find_sidlo(c, elem, primary_sql_key)
                prokurista_fo_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element, adresa_id)
                c.execute("INSERT INTO prokuriste (company_id, zapis_datum, vymaz_datum, prokurista_fo_id, adresa_id, text_prokurista) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, prokurista_fo_id, adresa_id, text_prokurista,))
            else:
                zapis_datum = str(get_prop(elem, "zapisDatum"))
                vymaz_datum = str(get_prop(elem, "vymazDatum"))
                prokura_text = str(get_prop(elem, "hodnotaText"))
                c.execute("INSERT INTO prokura_common_texts (company_id, zapis_datum, vymaz_datum, prokura_text) VALUES (?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, prokura_text,)) 
    except Exception as f:
        print(f)

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
                adresa_id = find_sidlo(c, elem, primary_sql_key)
                akcionar_po_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
                c.execute("INSERT into jediny_akcionar (company_id, zapis_datum, vymaz_datum, text_akcionar, akcionar_po_id, adresa_id) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, text_akcionar, akcionar_po_id, adresa_id,))
            elif typ_akcionar == "F":
                adresa_id = find_sidlo(c, elem, primary_sql_key)
                akcionar_fo_id = find_fyzicka_osoba(c, ICO, elem, conn, primary_sql_key, element, adresa_id)
                c.execute("INSERT into jediny_akcionar (company_id, zapis_datum, vymaz_datum, text_akcionar, akcionar_fo_id, adresa_id) VALUES (?, ?, ?, ?, ?, ?)", (primary_sql_key, zapis_datum, vymaz_datum, text_akcionar, akcionar_fo_id, adresa_id,))    
    except Exception as f:
        print(f)

def find_insolvency(c, ICO, insolvency_elem, conn, primary_sql_key):
   try:
       my_iter = insolvency_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
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

def find_konkurz(c, ICO, konkurz_elem, conn, primary_sql_key):
   try:
       my_iter = konkurz_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
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

def find_sidlo(c, elem, primary_sql_key):
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
        c.execute("SELECT * FROM adresy_v2 WHERE stat = (?) and obec = (?) and ulice = (?) and castObce = (?) and cisloPo = (?) and cisloOr = (?) and psc = (?) and okres = (?) and komplet_adresa = (?) and cisloEv = (?) and cisloText = (?)", (statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText,))
        sidlo_id = c.fetchone()
        if sidlo_id == None:
            c.execute("INSERT INTO adresy_v2 (stat, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, komplet_adresa, cisloEv, cisloText) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (statNazev, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, adresaText, cisloEv, cisloText))
            address_key = c.lastrowid
        else:
            address_key = sidlo_id[0]
        return address_key
    except Exception as e:
        print(e)

def insert_relation_information_v2(c, elem, primary_sql_key, ancillary_table_key, zapis_datum, vymaz_datum):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(NULL, ?, ?, ?, ?)", (primary_sql_key, ancillary_table_key,zapis_datum, vymaz_datum,))
    except Exception as f:
        print(f)
    return 0

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

def get_relationship_table_key(c, primary_sql_key, ancillary_table_key):
    c.execute("SELECT id FROM statutarni_organ_relation WHERE company_id = (?) and statutarni_organ_id = (?)", (primary_sql_key,ancillary_table_key,))
    return c.fetchone()[0]

def find_pocet_clenu(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        pocet_clenu_number = str(get_prop(elem, "hodnotaText"))
        c.execute("INSERT into pocty_clenu_organu (organ_id, pocet_clenu_value, zapis_datum, vymaz_datum) VALUES (?,?,?,?)", (relationship_table_key, pocet_clenu_number, zapis_datum, vymaz_datum,))        
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
            adresa_id = find_sidlo(c, elem, relationship_table_key)
            osoba_id = find_fyzicka_osoba(c, ICO, elem, conn, relationship_table_key, element, adresa_id)
            c.execute("INSERT into statutarni_organ_clen_relation (statutarni_organ_id, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (?,?,?,?,?,?,?,?,?,?)", (relationship_table_key, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
        if typ_osoby == "AngazmaPravnicke":
            spol_ico = str(get_prop(elem, "osoba/ico"))
            regCislo = str(get_prop(elem, "osoba/regCislo"))
            adresa_id = find_sidlo(c, elem, relationship_table_key)
            prav_osoba_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
            c.execute("INSERT into statutarni_organ_clen_relation (statutarni_organ_id, prav_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (?,?,?,?,?,?,?,?,?,?)", (relationship_table_key, prav_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
    except Exception as f:
        print(f)

def insert_individual_relations_v2(c, ICO, conn, primary_sql_key, zapis_datum, vymaz_datum, hodnota_text):
    insert_into_ancillary_table(c, elem, inserted_figure)
    return 0

def find_fyzicka_osoba(c, ICO, elem, conn, relationship_table_key, element, adresa_id):
    try:
        jmeno = lower_names_chars(str(get_prop(elem, "osoba/jmeno")))
        prijmeni = lower_names_chars(str(get_prop(elem, "osoba/prijmeni")))
        datum_narozeni = str(get_prop(elem, "osoba/narozDatum"))
        titulPred = str(get_prop(elem, "osoba/titulPred"))
        titulZa = str(get_prop(elem, "osoba/titulZa"))
        insert_fyzicka_osoba(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id)
        osoba_id = find_osoba_id(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id)
        return osoba_id
    except:
        pass

def lower_names_chars(string_name):
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
        c.execute("INSERT into fyzicke_osoby (titul_pred, jmeno, prijmeni, titul_za, datum_naroz, adresa_id) VALUES (?,?,?,?,?,?)", (titulPred, jmeno, prijmeni, titulZa, datum_narozeni,adresa_id,))
    except:
        pass

def find_osoba_id(c, titulPred, jmeno, prijmeni, titulZa, datum_narozeni, adresa_id):
    try:
        anciallary_table_key = c.execute("SELECT id FROM fyzicke_osoby WHERE titul_pred = (?) and jmeno = (?) and prijmeni = (?) and titul_za = (?) and datum_naroz = (?) and adresa_id = (?)", (titulPred, jmeno, prijmeni, titulZa, datum_narozeni,adresa_id,))
        anciallary_table_key = c.fetchone()[0]
        return anciallary_table_key
    except Exception as f:
        print(f) 

def find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id):
    try:
        nazev = str(get_prop(elem, "osoba/nazev"))
        insert_pravnicka_osoba(c, elem, spol_ico, regCislo, nazev, adresa_id)
        osoba_id = find_pravnicka_osoba_id(c, spol_ico, regCislo, nazev, adresa_id)
        return osoba_id
    except Exception as f:
        print(f)

def find_pocet_clenu_dr(c, ICO, elem, conn, relationship_table_key, element):
    try:
        zapis_datum = str(get_prop(elem, "zapisDatum"))
        vymaz_datum = str(get_prop(elem, "vymazDatum"))
        pocet_clenu_number = str(get_prop(elem, "hodnotaText"))
        c.execute("INSERT into pocty_clenu_DR (organ_id, pocet_clenu_value, zapis_datum, vymaz_datum) VALUES (?,?,?,?)", (relationship_table_key, pocet_clenu_number, zapis_datum, vymaz_datum,))        
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
            adresa_id = find_sidlo(c, elem, relationship_table_key)
            osoba_id = find_fyzicka_osoba(c, ICO, elem, conn, relationship_table_key, element, adresa_id)
            c.execute("INSERT into dr_organ_clen_relation (dozorci_rada_id, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (?,?,?,?,?,?,?,?,?,?)", (relationship_table_key, osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
        elif typ_osoby == "AngazmaPravnicke":
            spol_ico = str(get_prop(elem, "osoba/ico"))
            regCislo = str(get_prop(elem, "osoba/regCislo"))
            adresa_id = find_sidlo(c, elem, relationship_table_key)
            pravnicka_osoba_id = find_pravnicka_osoba(c, elem, spol_ico, regCislo, adresa_id)
            c.execute("INSERT into dr_organ_clen_relation (dozorci_rada_id, pravnicka_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkce_od, funkce_do, clenstvi_od, clenstvi_do, funkce) VALUES (?,?,?,?,?,?,?,?,?,?)", (relationship_table_key, pravnicka_osoba_id, adresa_id, zapis_datum, vymaz_datum, funkceOd, funkceDo, clenstviOd, clenstviDo, funkce_statutar_organu,))
    except Exception as f:
        print(f)

# TODO MERGE THESE THREE FUNCTIONS INTO ONE
def insert_podily(c, elem, spolecnik_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            zapisDatum = str(get_prop(podil_elem, "zapisDatum"))
            vymazDatum = str(get_prop(podil_elem, "vymazDatum"))
            druh_podilu_id = get_druh_podilu_id(c, podil_elem)
            vklad_typ = str(get_prop(podil_elem, "hodnotaUdaje/vklad/typ"))
            vklad_text = str(get_prop(podil_elem, "hodnotaUdaje/vklad/textValue"))
            souhrn_typ = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/typ"))
            souhrn_text = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue"))
            splaceni_typ = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/typ"))
            splaceni_text = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue"))
            c.execute("INSERT INTO podily (spolecnik_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (?,?,?,?,?,?,?,?,?,?)", (spolecnik_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
    except Exception as f:
        print(f)

def insert_vacant_podily(c, elem, vacant_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            zapisDatum = str(get_prop(podil_elem, "zapisDatum"))
            vymazDatum = str(get_prop(podil_elem, "vymazDatum"))
            druh_podilu_id = get_druh_podilu_id(c, podil_elem)
            vklad_typ = str(get_prop(podil_elem, "hodnotaUdaje/vklad/typ"))
            vklad_text = str(get_prop(podil_elem, "hodnotaUdaje/vklad/textValue"))
            souhrn_typ = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/typ"))
            souhrn_text = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue"))
            splaceni_typ = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/typ"))
            splaceni_text = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue"))
            c.execute("INSERT INTO podily (uvolneny_podil_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (?,?,?,?,?,?,?,?,?,?)", (vacant_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
    except Exception as f:
        print(f)    

def insert_common_podily(c, elem, common_id):
    try:
        podil_iter = elem.findall("podudaje/Udaj")
        for podil_elem in podil_iter:
            if str(get_prop(podil_elem, "udajTyp/kod")) == "SPOLECNIK_PODIL":
                zapisDatum = str(get_prop(podil_elem, "zapisDatum"))
                vymazDatum = str(get_prop(podil_elem, "vymazDatum"))
                druh_podilu_id = get_druh_podilu_id(c, podil_elem)
                vklad_typ = str(get_prop(podil_elem, "hodnotaUdaje/vklad/typ"))
                vklad_text = str(get_prop(podil_elem, "hodnotaUdaje/vklad/textValue"))
                souhrn_typ = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/typ"))
                souhrn_text = str(get_prop(podil_elem, "hodnotaUdaje/souhrn/textValue"))
                splaceni_typ = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/typ"))
                splaceni_text = str(get_prop(podil_elem, "hodnotaUdaje/splaceni/textValue"))
                c.execute("INSERT INTO podily (spolecny_podil_id, zapis_datum, vymaz_datum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text) VALUES (?,?,?,?,?,?,?,?,?,?)", (common_id, zapisDatum, vymazDatum, druh_podilu_id, vklad_typ, vklad_text, souhrn_typ, souhrn_text, splaceni_typ, splaceni_text,))
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

def find_pravnicka_osoba_id(c, spol_ico, regCislo, nazev, adresa_id):
    try:
        anciallary_table_key = c.execute("SELECT id FROM pravnicke_osoby WHERE ico = (?) and reg_cislo = (?) and nazev = (?) and adresa_id = (?)", (spol_ico, regCislo, nazev, adresa_id))
        anciallary_table_key = c.fetchone()[0]
        return anciallary_table_key
    except Exception as f:
        print(f) 

def insert_pravnicka_osoba(c, elem, spol_ico, regCislo, nazev, adresa_id):
    try:
        c.execute("INSERT into pravnicke_osoby (ico, reg_cislo, nazev, adresa_id) VALUES (?,?,?, ?)", (spol_ico, regCislo, nazev, adresa_id,))
    except:
        pass

def get_prop(element, prop):
    try:
        return element.find(prop).text
    except:
        return "0"