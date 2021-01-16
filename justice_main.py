# -*- coding: utf-8 -*-

# import cProfile
# import xml.etree.ElementTree as et
# import time
import requests
import shutil
from lxml import etree
import sqlite3
import gzip
import send2trash
import os
from datetime import datetime

# The function opens a file and parses the extracted data into the database
def parse_to_DB(file):
    print("Processing ", str(file))
    conn = sqlite3.connect('justice_v4.db')
    c = conn.cursor()
    for event, element in etree.iterparse(file, tag="Subjekt"):
        # Bugfix for companies which have been deleted but appear in the list of existing companies      
        if ([element.find('vymazDatum')][0]) != None:
            continue
        else:
            ICO = get_ICO(element)
            sidlo_set = False
            # print(ICO)
            # Vlozit prazdny radek s ICO
            insert_new_ICO(c, ICO, conn)
            # Vlozit jednolive parametry
            insert_prop(c, get_prop(element, "nazev"), conn, ICO, "nazev")
            insert_prop(c, get_prop(element, "zapisDatum"), conn, ICO, "zapis")
            insert_prop(c, get_prop(element, "vymazDatum"), conn, ICO, "vymaz")
            insert_prop(c, get_prop(element, ".//udaje/Udaj/spisZn/oddil"), conn, ICO, "oddil")
            insert_prop(c, get_prop(element, ".//udaje/Udaj/spisZn/vlozka"), conn, ICO, "vlozka")
            insert_prop(c, get_prop(element, ".//udaje/Udaj/spisZn/soud/kod"), conn, ICO, "soud")
            insert_prop(c, str(adresa(get_SIDLO_v2(element))), conn, ICO, "sidlo")
            
            # insert_prop(c, get_prop(element, ".//udaje/Udaj/adresa/obec"), conn, ICO, "sidlo")
            # insert_prop(c, str(adresa(get_SIDLO(".//udaje/Udaj/adresa"))), conn, ICO, "sidlo")
            # insert_prop(c, get_prop(element, ".//udaje/Udaj/adresa"), conn, ICO, "sidlo")
            # Now, I need to go deeper into the file to extract data about the registered office
            # subjekt_udaje = element.findall('.//Udaj')
            # for udaj in subjekt_udaje:
            #     udaje_spolecnosti = udaj.findall(".//kod")
            #     if "SIDLO" in udaje_spolecnosti[0].text and sidlo_set == False:
            #                 try:
            #                     insert_prop(c, str(adresa(get_SIDLO(udaj))), conn, ICO, "sidlo")
            #                     # print(sidlo)
            #                     # spolecnosti2[ICO].set_SIDLO(get_SIDLO(udaj,udaje_spolecnosti))
                                
            #                     # c.execute("UPDATE spolecnosti SET sidlo = (?) WHERE ICO = (?)", (str(get_SIDLO(udaj,udaje_spolecnosti)), ICO,))
            #                     # conn.commit()
            #                     sidlo_set = True
            #                 except:
            #                     print("Zkusil jsem to a nevyslo to!")
            #                     sidlo_set = False
                
            element.clear()
            # subjekt_udaje.clear()
    conn.commit()
    conn.close()
    return 0

# Function to attempt to insert a placeholder for a new company based on ICO
def insert_new_ICO(c, ICO, conn):
    try:
        c.execute("INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ICO, "", "", "", "", "", "", ""))
        # conn.commit()
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
    except:
        pass

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
    
    # stat = get_prop(element, ".//udaje/Udaj/adresa/statNazev")
    # obec = get_prop(element, ".//udaje/Udaj/adresa/obec")
    # ulice = get_prop(element, ".//udaje/Udaj/adresa/ulice")
    # castObce = get_prop(element, ".//udaje/Udaj/adresa/castObce")
    # cisloPo = get_prop(element, ".//udaje/Udaj/adresa/cisloPo")
    # cisloOr = get_prop(element, ".//udaje/Udaj/adresa/cisloOr")
    # psc = get_prop(element, ".//udaje/Udaj/adresa/psc")
    # okres = get_prop(element, ".//udaje/Udaj/adresa/okres")
    # komplet_adresa = get_prop(element, ".//udaje/Udaj/adresa/adresaText") 
    # cisloEv = get_prop(element, ".//udaje/Udaj/adresa/cisloEv")
    # cisloText = get_prop(element, ".//udaje/Udaj/adresa/cisloText")
    
        
    
    # if address_field[0] != "Česká republika":
    #     print(address_field)
    return address_field    
    # print([stat, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, komplet_adresa, cisloEv, cisloText])
        
    # return [stat, obec, ulice, castObce, cisloPo, cisloOr, psc, okres, komplet_adresa, cisloEv, cisloText]

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
                    if self.psc != None:
                        return str(self.obec + " " + self.cisloText + " " + "okres " +  self.okres + ", PSČ " + self.psc)
                    else:
                        return str(self.obec + " " + self.cisloText + " " + "okres " +  self.okres)
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
                            return str(self.obec + ", " + self.ulice + " " + srovnat_obec_cast(self.obec, self.castObce) + ", PSČ" + self.psc + " " + self.stat)
                        else:
                            return str(self.obec + ", " + self.ulice + " " + srovnat_obec_cast(self.obec, self.castObce) + " " + self.stat)
                    else:
                        return str(self.ulice + " č.ev. " + self.cisloEv + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)    
                else:
                    if self.psc != None:
                        return str(self.ulice + " " + self.cisloPo + ", " + srovnat_obec_cast(self.obec, self.castObce) + ", " + self.psc + " " + self.obec + ", " + self.stat)           
                    else:
                        return str(self.ulice + " " + self.cisloPo + ", " + srovnat_obec_cast(self.obec, self.castObce) + " " + self.obec + ", " + self.stat)         
            
            if self.cisloPo == None and self.cisloEv != None:
                return str(self.obec + " č.ev. " + self.cisloEv + ", " + self.psc + srovnat_obec_cast(self.obec, self.castObce) + " " + self.obec + ", " + self.stat)
            
            if self.cisloPo != None:
                return str("č.p. " + self.cisloPo + ", " + self.psc + srovnat_obec_cast(self.obec, self.castObce) + " " + self.obec + ", " + self.stat)
            
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
                update_data(osoba + "-actual-" + soud + "-" + rok + ".xml.gz")
            elif method == "db_update":
                try:
                    parse_to_DB(os.path.join(str(os.getcwd()), "data", osoba) + "-actual-" + soud + "-" + rok + ".xml")
                except:
                    pass
            # print(osoba + "-actual-" + soud + "-" + rok + ".xml")

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


# parse_to_DB("as-actual-ostrava-2020-simple.xml")

# parse_to_DB("as-actual-praha-2020.xml")

# parse_to_DB("sro-actual-praha-2020.xml")

def do_both():
    # general_update("down")
    general_update("db_update")

do_both()

# cProfile.run('do_both()')
