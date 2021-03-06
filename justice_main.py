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
    conn = sqlite3.connect('justice.db')
    c = conn.cursor()
    for event, element in etree.iterparse(file, tag="Subjekt"):
        # Bugfix for companies which have been deleted but appear in the list of existing companies      
        if ([element.find('vymazDatum')][0]) != None:
            continue
        else:
            ICO = get_ICO(element)
            # Vlozit prazdny radek s ICO
            insert_new_ICO(c, ICO, conn)
            primary_sql_key = get_primary_sql_key(c, ICO)
            # Vlozit jednolive parametry
            insert_primary_company_figures(c, ICO, element, conn)
            insert_company_relations(c, ICO, element, conn, primary_sql_key)
            # insert_obec_relation(c, conn, ICO, element, primary_sql_key)                
            find_other_properties(c, ICO, element, conn, primary_sql_key)
            element.clear()
            
            # subjekt_udaje.clear()

    # purge_DB(c)
    conn.commit()
    conn.close()
    return 0

def purge_DB(c):
    c.execute("DELETE FROM companies")
    c.execute("DELETE FROM obce")
    c.execute("DELETE FROM ulice")
    c.execute("DELETE FROM ulice_relation")
    c.execute("DELETE FROM osoby")
    c.execute("DELETE FROM obce_relation")
    c.execute("DELETE FROM sqlite_sequence")
    c.execute("DELETE FROM pravni_formy")
    c.execute("DELETE FROM pravni_formy_relation")

def find_other_properties(c, ICO, element, conn, primary_sql_key):
    try:
        my_iter = element.iter("udaje")
        for elem in my_iter:
            my_iter2 = elem.iter("Udaj")
            for elem2 in my_iter2:
                # print(ICO, str(get_prop(elem2, ".//udajTyp/kod")))
                if str(get_prop(elem2, ".//udajTyp/kod")) == "INSOLVENCE_SEKCE":
                    # print("INSOLVENCY:", ICO)
                    find_active_insolvency(c, ICO, elem2, conn, primary_sql_key)
                elif str(get_prop(elem2, ".//udajTyp/kod")) == "KONKURS_SEKCE":
                    find_active_insolvency(c, ICO, elem2, conn, primary_sql_key)
    except:
        pass

def find_active_insolvency(c, ICO, insolvency_elem, conn, primary_sql_key):
   try:
       my_iter = insolvency_elem.findall("podudaje")
       for elem in my_iter:
           my_iter2 = elem.iter("Udaj")
           for elem2 in my_iter2:
               if (str(get_prop(elem2, ".//vymazDatum"))) == "0":
                   insolvency_text = str(get_prop(elem2, ".//text"))
                   if insolvency_text != "0":
                       insert_insolvency_text(c, conn, insolvency_text, primary_sql_key)
                       # print(insolvency_text)
                   # print(ICO, str(get_prop(elem2, ".//zapisDatum")), str(get_prop(elem2, ".//text")))
                # my_iter3 = elem2.iterfind()
                # for elem3 in my_iter3:
                   # print(str(get_prop(elem2, ".//hlavicka")))
                   # print(str(get_prop(elem2, ".//zapisDatum")))
                   # print(str(get_prop(elem2, ".//vymazDatum")))
   except:
       pass

def insert_insolvency_text(c, conn, insolvency_text, primary_sql_key):
    try:
        c.execute("INSERT INTO insolvency_events (company_id, insolvency_event) VALUES(?, ?)", (primary_sql_key, insolvency_text,))
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
    insert_instructions = [("nazev","nazev"), ("zapisDatum","zapis"), (".//udaje/Udaj/spisZn/oddil","oddil"),
                           (".//udaje/Udaj/spisZn/vlozka","vlozka"),(".//udaje/Udaj/spisZn/soud/kod","soud"),(str(adresa(get_SIDLO_v2(element))),"sidlo")]
    for elem in insert_instructions[:-1]:
        insert_prop(c, get_prop(element, elem[0]), conn, ICO, elem[1])
    # Override to insert the address
    insert_prop(c, insert_instructions[-1][0], conn, ICO, insert_instructions[-1][1])
    return 0

def insert_company_relations(c, ICO, element, conn, primary_sql_key):
    insert_instructions = [(".//udaje/Udaj/adresa/obec","obce", "obec_jmeno", "obce_relation"), (".//udaje/Udaj/adresa/ulice","ulice", "ulice_jmeno", "ulice_relation"),
                           (".//udaje/Udaj/pravniForma/nazev","pravni_formy", "pravni_forma", "pravni_formy_relation")]
    for elem in insert_instructions:
        insert_individual_relations(c, ICO, element, conn, primary_sql_key, elem)
    return 0

def insert_individual_relations(c, ICO, element, conn, primary_sql_key, elem):
    inserted_figure = str(get_prop(element, elem[0]))
    insert_into_ancillary_table(c, elem, inserted_figure)
    ancillary_table_key = get_anciallary_table_key(c, elem, inserted_figure)
    insert_relation_information(c, elem, primary_sql_key, ancillary_table_key)
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
    except:
        print("Nepovedlo se")
        return 0

def insert_relation_information(c, elem, primary_sql_key, ancillary_table_key):
    try:
        c.execute("INSERT INTO " + elem[3] + " VALUES(?, ?)", (primary_sql_key, ancillary_table_key,))
    except:
        pass
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
def insert_new_ICO(c, ICO, conn):
    
    try:
        c.execute("INSERT INTO companies (ico) VALUES (?);", (ICO,))
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
                            return str(self.obec + ", " + self.ulice + "" + srovnat_obec_cast(self.obec, self.castObce) + ", PSČ" + self.psc + " " + self.stat)
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
                update_data(osoba + "-actual-" + soud + "-" + rok + ".xml.gz")
            elif method == "db_update":
                try:
                    parse_to_DB(os.path.join(str(os.getcwd()), "data", osoba) + "-actual-" + soud + "-" + rok + ".xml")
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


# parse_to_DB("as-full-praha-2021.xml")

# parse_to_DB("ks-actual-ostrava-2021.xml")

# parse_to_DB("sro-actual-praha-2020.xml")

def do_both():
        general_update("down")
        general_update("db_update")

do_both()

# cProfile.run('do_both()')
