import sqlite3

def create_DB(conn):
    # create_DB_file(db_file)
    # conn = create_connection(db_file)
    create_tables(conn)
    # create_indices(conn)
    conn.commit()
    # conn.close()

# def create_DB_file(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#     except Exception as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Exception as e:
#         print(e)
#     return conn

def create_tables(conn):
    list_of_tables = []
    companies = """CREATE TABLE companies (
	    id SERIAL PRIMARY KEY, 
	    ico	TEXT NOT NULL UNIQUE, 
	    nazev TEXT, 
	    zapis DATE, 
	    oddil TEXT, 
	    vlozka TEXT, 
	    soud TEXT)"""
    list_of_tables.append(companies)
    
#     adresy_v2 = """ CREATE TABLE "adresy_v2" (
# 	id              SERIAL PRIMARY KEY, 
# 	stat	        TEXT,
# 	obec	        TEXT,
# 	ulice	        TEXT,
# 	castObce	    TEXT,
# 	cisloPo	        TEXT,
# 	cisloOr	        TEXT,
# 	psc	            TEXT,
# 	okres   	    TEXT,
# 	komplet_adresa	TEXT,
# 	cisloEv	        TEXT,
# 	cisloText	    TEXT,
#     CONSTRAINT not_distinct_address UNIQUE NULLS NOT DISTINCT ("stat","obec","ulice","castobce","cislopo","cisloor","psc","okres","komplet_adresa","cisloev","cislotext"),
# 	CONSTRAINT unique_address UNIQUE("stat","obec","ulice","castobce","cislopo","cisloor","psc","okres","komplet_adresa","cisloev","cislotext")
# ); """
#     list_of_tables.append(adresy_v2)


    adresy_v2 = """ CREATE TABLE "adresy_v2" (
	id              SERIAL PRIMARY KEY, 
	stat	        TEXT,
	obec	        TEXT,
	ulice	        TEXT,
	castobce	    TEXT,
	cislopo	        TEXT,
	cisloor	        TEXT,
	psc	            TEXT,
	okres   	    TEXT,
	komplet_adresa	TEXT,
	cisloev	        TEXT,
	cislotext	    TEXT,
    CONSTRAINT not_distinct_address UNIQUE NULLS NOT DISTINCT (stat,obec,ulice,castobce,cislopo,cisloor,psc,okres,komplet_adresa,cisloev,cislotext)    
); """
    list_of_tables.append(adresy_v2)


#     fyzicke_osoby = """ CREATE TABLE "fyzicke_osoby" (
# 	"id"	SERIAL PRIMARY KEY,
# 	"titul_pred"	TEXT,
# 	"jmeno"	TEXT,
# 	"prijmeni"	TEXT,
# 	"titul_za"	TEXT,
# 	"datum_naroz"	TEXT,
# 	"adresa_id" INTEGER,
# 	CONSTRAINT not_distinct_natural_person UNIQUE NULLS NOT DISTINCT ("titul_pred","jmeno","prijmeni","titul_za","datum_naroz","adresa_id"),
# 	CONSTRAINT unique_natural_person UNIQUE ("titul_pred","jmeno","prijmeni","titul_za","datum_naroz","adresa_id"),
# 	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id")
# ); """
#     list_of_tables.append(fyzicke_osoby)


    fyzicke_osoby = """ CREATE TABLE "fyzicke_osoby" (
	"id"	SERIAL PRIMARY KEY,
	"titul_pred"	TEXT,
	"jmeno"	TEXT,
	"prijmeni"	TEXT,
	"titul_za"	TEXT,
	"datum_naroz"	DATE,
	"adresa_id" INTEGER,
	CONSTRAINT not_distinct_natural_person UNIQUE NULLS NOT DISTINCT ("titul_pred","jmeno","prijmeni","titul_za","datum_naroz","adresa_id"),
	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id")
); """
    list_of_tables.append(fyzicke_osoby)


#     pravnicke_osoby = """ CREATE TABLE "pravnicke_osoby" (
# 	"id"	SERIAL PRIMARY KEY,
# 	"ico"	TEXT,
# 	"reg_cislo"	TEXT,
# 	"nazev"	TEXT,
# 	"adresa_id" INTEGER,
# 	CONSTRAINT not_distinct_legal_person UNIQUE NULLS NOT DISTINCT ("ico","reg_cislo","nazev","adresa_id"),
# 	CONSTRAINT unique_legal_person UNIQUE("ico","reg_cislo","nazev","adresa_id"),
# 	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id")
# ); """
#     list_of_tables.append(pravnicke_osoby)


    pravnicke_osoby = """ CREATE TABLE "pravnicke_osoby" (
	"id"	SERIAL PRIMARY KEY,
	"ico"	TEXT,
	"reg_cislo"	TEXT,
	"nazev"	TEXT,
	"adresa_id" INTEGER,
	CONSTRAINT not_distinct_legal_person UNIQUE NULLS NOT DISTINCT ("ico","reg_cislo","nazev","adresa_id"),
	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id")
); """
    list_of_tables.append(pravnicke_osoby)
    


    spolecnici_uvolneny_podil = """ CREATE TABLE "spolecnici_uvolneny_podil" (
	"id" SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"text_uvolneny_podil"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(spolecnici_uvolneny_podil)

    spolecnici_spolecny_podil = """ CREATE TABLE "spolecnici_spolecny_podil" (
	"id" SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"text_spolecny_podil"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(spolecnici_spolecny_podil)

    akcie = """ CREATE TABLE "akcie" (
	"id"	        SERIAL PRIMARY KEY, 
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"akcie_podoba"	TEXT,
	"akcie_typ"	TEXT,
	"akcie_pocet"	TEXT,
	"akcie_hodnota_typ"	TEXT,
	"akcie_hodnota_value"	TEXT,
	"akcie_text"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(akcie)

    criminal_records = """ CREATE TABLE "criminal_records" (
	"id" 				SERIAL PRIMARY KEY,
	"company_id"		INTEGER NOT NULL,
	"first_instance"	TEXT,
	"second_instance"	TEXT,
	"paragraphs"		TEXT,
	"penalties"			TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
	) """
    list_of_tables.append(criminal_records)

    dr_relation = """ CREATE TABLE "dozorci_rada_relation" (
	"id"	        SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(dr_relation)

    dr_organ_clen_relation = """ CREATE TABLE "dr_organ_clen_relation" (
	"id"	SERIAL PRIMARY KEY,
	"dozorci_rada_id"	INTEGER NOT NULL,
	"osoba_id"	INTEGER,
	"pravnicka_osoba_id" INTEGER,
	"adresa_id"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"funkce_od"	DATE,
	"funkce_do"	DATE,
	"clenstvi_od"	DATE,
	"clenstvi_do"	DATE,
	"funkce"	TEXT,
	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id"),
	FOREIGN KEY("dozorci_rada_id") REFERENCES "dozorci_rada_relation"("id"),
	FOREIGN KEY("osoba_id") REFERENCES "fyzicke_osoby"("id")
); """
    list_of_tables.append(dr_organ_clen_relation)

    druhy_podilu = """ CREATE TABLE "druhy_podilu" (
	"id"			SERIAL PRIMARY KEY,
	"druh_podilu"	TEXT NOT NULL
); """
    list_of_tables.append(druhy_podilu)

    insolvency_events = """ CREATE TABLE "insolvency_events" (
	"id"	        SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"insolvency_event"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(insolvency_events)

    jediny_akcionar = """ CREATE TABLE "jediny_akcionar" (
	"id"	        SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"text_akcionar"	TEXT,
	"akcionar_po_id"	INTEGER,
	"akcionar_fo_id"	INTEGER,
	"adresa_id"	INTEGER,
	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("akcionar_po_id") REFERENCES "pravnicke_osoby"("id"),
	FOREIGN KEY("akcionar_fo_id") REFERENCES "fyzicke_osoby"("id")
); """
    list_of_tables.append(jediny_akcionar)

    konkurz_events = """ CREATE TABLE "konkurz_events" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"konkurz_event"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(konkurz_events)

    nazvy = """ CREATE TABLE "nazvy" (
	"id"	        SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"nazev_text"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(nazvy)

    ostatni_skutecnosti = """ CREATE TABLE "ostatni_skutecnosti" (
	"id"        	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"ostatni_skutecnost"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(ostatni_skutecnosti)

    pocty_clenu_dr = """ CREATE TABLE "pocty_clenu_dr" (
	"id"	SERIAL PRIMARY KEY,
	"organ_id"	INTEGER NOT NULL,
	"pocet_clenu_value"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("organ_id") REFERENCES "dozorci_rada_relation"("id")
); """
    list_of_tables.append(pocty_clenu_dr)

    spolecnici = """ CREATE TABLE "spolecnici" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"spolecnik_fo_id"	INTEGER,
	"spolecnik_po_id"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"adresa_id"	INTEGER,
	"text_spolecnik"	TEXT
); """
    list_of_tables.append(spolecnici)

    podilnici = """ CREATE TABLE "podilnici" (
	"id"	SERIAL PRIMARY KEY,
	"podil_id"	INTEGER,
	"podilnik_fo_id"	INTEGER,
	"podilnik_po_id"	INTEGER,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"adresa_id"	INTEGER
); """
    list_of_tables.append(podilnici)

    podily = """ CREATE TABLE "podily" (
	"id"				SERIAL PRIMARY KEY,
	"spolecnik_id"		INTEGER,
	"uvolneny_podil_id" INTEGER,
	"spolecny_podil_id" INTEGER,
	"zapis_datum"		DATE,
	"vymaz_datum"		DATE,
	"druh_podilu_id"	INTEGER,
	"vklad_typ"			TEXT,
	"vklad_text"		TEXT,
	"souhrn_typ"		TEXT,
	"souhrn_text"		TEXT,
	"splaceni_typ"		TEXT,
	"splaceni_text"		TEXT
); """
    list_of_tables.append(podily)

    zastavy = """ CREATE TABLE "zastavy" (
    "id"				SERIAL PRIMARY KEY,
    "podil_id"			INTEGER,
    "zapis_datum"		DATE,
	"vymaz_datum"		DATE,
    "zastava_text"		TEXT
); """
    list_of_tables.append(zastavy)

    pravni_formy = """ CREATE TABLE "pravni_formy" (
	"id"	SERIAL PRIMARY KEY,
	"pravni_forma"	TEXT NOT NULL UNIQUE
); """
    list_of_tables.append(pravni_formy)

    pravni_formy_relation = """ CREATE TABLE "pravni_formy_relation" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"pravni_forma_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	FOREIGN KEY("pravni_forma_id") REFERENCES "pravni_formy"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
    ); """
    list_of_tables.append(pravni_formy_relation)

    sidlo_relation = """ CREATE TABLE "sidlo_relation" (
    id	            SERIAL PRIMARY KEY,
    company_id	    INTEGER NOT NULL,
    sidlo_id	    INTEGER NOT NULL,
    zapis_datum	    DATE,
    vymaz_datum	    DATE,
    CONSTRAINT fk_company
        FOREIGN KEY(company_id)  
            REFERENCES companies(id),
    CONSTRAINT fk_sidlo       
        FOREIGN KEY(sidlo_id) 
            REFERENCES adresy_v2(id)
    ); """
    list_of_tables.append(sidlo_relation)

    predmety_cinnosti = """ CREATE TABLE "predmety_cinnosti" (
	"id"	SERIAL PRIMARY KEY,
	"predmet_cinnosti"	TEXT NOT NULL UNIQUE
); """
    list_of_tables.append(predmety_cinnosti)

    predmety_cinnosti_relation = """ CREATE TABLE "predmety_cinnosti_relation" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"predmet_cinnosti_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("predmet_cinnosti_id") REFERENCES "predmety_cinnosti"("id")
); """
    list_of_tables.append(predmety_cinnosti_relation)

    predmety_podnikani = """ CREATE TABLE "predmety_podnikani" (
	"id"	SERIAL PRIMARY KEY,
	"predmet_podnikani"	TEXT NOT NULL UNIQUE
); """
    list_of_tables.append(predmety_podnikani)

    predmety_podnikani_relation = """ CREATE TABLE "predmety_podnikani_relation" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"predmet_podnikani_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("predmet_podnikani_id") REFERENCES "predmety_podnikani"("id")
); """
    list_of_tables.append(predmety_podnikani_relation)

    prokura_common_texts = """ CREATE TABLE "prokura_common_texts" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"prokura_text"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(prokura_common_texts)

    prokuriste = """ CREATE TABLE "prokuriste" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"prokurista_fo_id"	INTEGER,
	"adresa_id"	INTEGER,
	"text_prokurista"	TEXT,
	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id"),
	FOREIGN KEY("prokurista_fo_id") REFERENCES "fyzicke_osoby"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(prokuriste)

    statutarni_organy = """ CREATE TABLE "statutarni_organy" (
	"id"	SERIAL PRIMARY KEY,
	"statutarni_organ_text"	TEXT NOT NULL UNIQUE
); """
    list_of_tables.append(statutarni_organy)

    statutarni_organ_relation = """ CREATE TABLE "statutarni_organ_relation" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"statutarni_organ_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("statutarni_organ_id") REFERENCES "statutarni_organy"("id"),
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(statutarni_organ_relation)

    pocty_clenu_organu = """ CREATE TABLE "pocty_clenu_organu" (
	"id"	SERIAL PRIMARY KEY,
	"organ_id"	INTEGER NOT NULL,
	"pocet_clenu_value"	INTEGER,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	FOREIGN KEY("organ_id") REFERENCES "statutarni_organ_relation"("id")
); """
    list_of_tables.append(pocty_clenu_organu)

    statutarni_organ_clen_relation = """ CREATE TABLE "statutarni_organ_clen_relation" (
	"id"	SERIAL PRIMARY KEY,
	"statutarni_organ_id"	INTEGER NOT NULL,
	"osoba_id"	INTEGER,
	"prav_osoba_id"	INTEGER,
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
	FOREIGN KEY("adresa_id") REFERENCES "adresy_v2"("id")
); """
    list_of_tables.append(statutarni_organ_clen_relation)

    ubo = """ CREATE TABLE "ubo" (
	"id" SERIAL PRIMARY KEY,
	"company_id"  INTEGER NOT NULL,
	"ubo_id" INTEGER NOT NULL,
	"adresa_id" INTEGER,
	"zapis_datum"  DATE,
	"vymaz_datum"  DATE,
	"postaveni" TEXT,
	"koncovy_prijemce_text" TEXT,
	"skutecnym_majitelem_od" TEXT,
	"vlastni_podil_na_prospechu" TEXT,
	"vlastni_podil_na_prospechu_typ" TEXT,
	"vlastni_podil_na_prospechu_text_value" TEXT,
	"vlastni_podil_na_hlasovani" TEXT,
	"vlastni_podil_na_hlasovani_typ" TEXT,
	"vlastni_podil_na_hlasovani_value" TEXT
); """
    list_of_tables.append(ubo)

    ucel = """ CREATE TABLE "ucel" (
	"id"	SERIAL PRIMARY KEY,
	"ucel"	TEXT NOT NULL UNIQUE
); """
    list_of_tables.append(ucel)

    ucel_relation = """ CREATE TABLE "ucel_relation" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"ucel_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("ucel_id") REFERENCES "ucel"("id")
); """
    list_of_tables.append(ucel_relation)

    zakladni_kapital = """ CREATE TABLE "zakladni_kapital" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	"vklad_typ"	TEXT,
	"vklad_hodnota"	TEXT,
	"splaceni_typ"	TEXT,
	"splaceni_hodnota"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(zakladni_kapital)

    zapis_soudy = """ CREATE TABLE "zapis_soudy" (
	"id"	SERIAL PRIMARY KEY,
	"company_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	"oddil"	TEXT,
	"vlozka"	TEXT,
	"soud"	TEXT,
	FOREIGN KEY("company_id") REFERENCES "companies"("id")
); """
    list_of_tables.append(zapis_soudy)

    zpusoby_jednani = """ CREATE TABLE "zpusoby_jednani" (
	"id"	SERIAL PRIMARY KEY,
	"zpusob_jednani_text"	TEXT UNIQUE
); """
    list_of_tables.append(zpusoby_jednani)

    zpusoby_jednani_relation = """ CREATE TABLE "zpusoby_jednani_relation" (
	"id"	SERIAL PRIMARY KEY,
	"statutarni_organ_id"	INTEGER NOT NULL,
	"zpusob_jednani_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE NOT NULL,
	"vymaz_datum"	DATE,
	FOREIGN KEY("zpusob_jednani_id") REFERENCES "zpusoby_jednani"("id"),
	FOREIGN KEY("statutarni_organ_id") REFERENCES "statutarni_organ_relation"("id")
); """
    list_of_tables.append(zpusoby_jednani_relation)

    # list_of_tables = [companies, adresy_v2, akcie, criminal_records, dr_relation, dr_organ_clen_relation, druhy_podilu, fyzicke_osoby, insolvency_events,
    # jediny_akcionar, konkurz_events, nazvy, ostatni_skutecnosti, pocty_clenu_DR, pocty_clenu_organu, podily, podilnici, pravni_formy,
    # pravni_formy_relation, pravnicke_osoby, predmety_cinnosti, predmety_cinnosti_relation, prdmety_podnikani, predmety_podnikani_relation,
    # prokura_common_texts, prokuriste, sidlo_relation, spolecnici, spolecnici_uvolneny_podil, spolecnici_spolecny_podil, statutarni_organ_clen_relation, statutarni_organ_relation, statutarni_organy, ubo,
    # ucel, ucel_relation, zakladni_kapital, zapis_soudy, zpusoby_jednani, zpusoby_jednani_relation]
    for elem in list_of_tables:
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(e)

def create_indices(conn):
    relevant_indices = []

    druhy_podilu = """ CREATE INDEX "index druh_podilu" ON "druhy_podilu" using HASH (
	"druh_podilu"
); """
    relevant_indices.append(druhy_podilu)

#     companies1 = """ CREATE INDEX "index companies1" ON "companies" (
# 	"id"
# ); """

    companies2 = """ CREATE INDEX "index companies2" ON "companies" (
	"ico"
); """
    relevant_indices.append(companies2)

#     companies3 = """ CREATE INDEX "index companies3" ON "companies" (
# 	"nazev"
# ); """

#     companies4 = """ CREATE INDEX "index companies4" ON "companies" (
# 	"oddil"
# ); """

#     companies5 = """ CREATE INDEX "index companies5" ON "companies" (
# 	"vlozka"
# ); """

#     adresy1 = """ CREATE INDEX "index adresy1" ON "adresy_v2" (
# 	"id"
# ); """

#     adresy2 = """ CREATE INDEX "index adresy2" ON "adresy_v2" using HASH (
# 	"obec"
# ); """
#     relevant_indices.append(adresy2)

#     adresy3 = """ CREATE INDEX "index adresy3" ON "adresy_v2" using HASH (
# 	"ulice"
# ); """
#     relevant_indices.append(adresy3)
    
#     adresy4 = """ CREATE INDEX "index adresy4" ON "adresy_v2" using HASH (
# 	"stat"
# ); """
#     relevant_indices.append(adresy4)
    
#     adresy5 = """ CREATE INDEX "index adresy5" ON "adresy_v2" using HASH (
# 	"castobce"
# ); """
#     relevant_indices.append(adresy5)
    
#     adresy6 = """ CREATE INDEX "index adresy12" ON "adresy_v2" using HASH (
# 	"cislopo"
# ); """
#     relevant_indices.append(adresy6)

#     adresy7 = """ CREATE INDEX "index adresy6" ON "adresy_v2" using HASH (
# 	"cisloor"
# ); """
#     relevant_indices.append(adresy7)
    
#     adresy8 = """ CREATE INDEX "index adresy7" ON "adresy_v2" using HASH (
# 	"psc"
# ); """
#     relevant_indices.append(adresy8)
    
#     adresy9 = """ CREATE INDEX "index adresy8" ON "adresy_v2" using HASH (
# 	"okres"
# ); """
#     relevant_indices.append(adresy9)
    
#     adresy10 = """ CREATE INDEX "index adresy9" ON "adresy_v2" using HASH (
# 	"komplet_adresa"
# ); """
#     relevant_indices.append(adresy10)
    
#     adresy11 = """ CREATE INDEX "index adresy10" ON "adresy_v2" using HASH (
# 	"cisloev"
# ); """
#     relevant_indices.append(adresy11)
    
#     adresy12 = """ CREATE INDEX "index adresy11" ON "adresy_v2" using HASH (
# 	"cislotext"
# ); """
#     relevant_indices.append(adresy12)
    

#     akcie = """ CREATE INDEX "index akcie1" ON "akcie" (
# 	"id"
# ); """

#     akcie2 = """ CREATE INDEX "index akcie2" ON "akcie" (
# 	"company_id"
# ); """

#     akcionari1 = """ CREATE INDEX "index akcionari1" ON "jediny_akcionar" (
# 	"id"
# ); """

#     akcionari2 = """ CREATE INDEX "index akcionari2" ON "jediny_akcionar" (
# 	"company_id"
# ); """

#     dr_clen_relation1 = """ CREATE INDEX "index dr clen relation1" ON "dr_organ_clen_relation" (
# 	"dozorci_rada_id"
# ); """

#     dr_clen_relation2 = """ CREATE INDEX "index dr clen relation2" ON "dr_organ_clen_relation" (
# 	"id"
# ); """

#     dr_relation = """ CREATE INDEX "index dr relation1" ON "dozorci_rada_relation" (
# 	"id"
# ); """

    dr_relation2 = """ CREATE INDEX "index dr relation2" ON "dozorci_rada_relation" (
	"company_id"
); """
    relevant_indices.append(dr_relation2)
#     insolvency1 = """ CREATE INDEX "index insolvency1" ON "insolvency_events" (
# 	"id"
# ); """

    insolvency2 = """ CREATE INDEX "index insolvency2" ON "insolvency_events" (
	"company_id"
); """
    relevant_indices.append(insolvency2)
#     konkurz1 = """CREATE INDEX "index konkurz1" ON "konkurz_events" (
# 	"company_id"
# ); """

#     konkurz2 = """CREATE INDEX "index konkurz2" ON "konkurz_events" (
# 	"id"
# ); """

#     nazvy1 = """ CREATE INDEX "index nazvy1" ON "nazvy" (
# 	"nazev_text"
# ); """

#     nazvy2 = """ CREATE INDEX "index nazvy2" ON "nazvy" (
# 	"company_id"
# ); """

#     nazvy3 = """ CREATE INDEX "index nazvy3" ON "nazvy" (
# 	"id"
# ); """

#     ostatni_skutecnosti = """ CREATE INDEX "index ostatni skutecnosti1" ON "ostatni_skutecnosti" (
# 	"company_id"
# ); """

#     ostatni_skutecnosti2 = """ CREATE INDEX "index ostatni skutecnosti2" ON "ostatni_skutecnosti" (
# 	"id"
# ); """

#     pocty_clenu_organ1 = """ CREATE INDEX "index pocty clenu org1" ON "pocty_clenu_organu" (
# 	"organ_id"
# ); """

#     pocty_clenu_organ2 = """ CREATE INDEX "index pocty clenu org2" ON "pocty_clenu_organu" (
# 	"id"
# ); """

    podily1 = """ CREATE INDEX "index podily1" ON "podily" (
	"id"
); """
    relevant_indices.append(podily1)

    podily2 = """ CREATE INDEX "index podily2" ON "podily" (
	"spolecnik_id"
); """
    relevant_indices.append(podily2)

    podily3 = """ CREATE INDEX "index podily3" ON "podily" (
	"uvolneny_podil_id"
); """
    relevant_indices.append(podily3)

    podily4 = """ CREATE INDEX "index podily4" ON "podily" (
	"spolecny_podil_id"
); """
    relevant_indices.append(podily4)

    podilnici1 = """ CREATE INDEX "index podilnici1" ON "podilnici" (
	"id"
); """
    relevant_indices.append(podilnici1)

    podilnici2 = """ CREATE INDEX "index podilnici2" ON "podilnici" (
	"podil_id"
); """
    relevant_indices.append(podilnici2)

    podilnici3 = """ CREATE INDEX "index podilnici3" ON "podilnici" (
	"podilnik_fo_id"
); """
    relevant_indices.append(podilnici3)

    podilnici4 = """ CREATE INDEX "index podilnici4" ON "podilnici" (
	"podilnik_po_id"
); """
    relevant_indices.append(podilnici4)

    podilnici5 = """ CREATE INDEX "index podilnici5" ON "podilnici" (
	"adresa_id"
); """
    relevant_indices.append(podilnici5)

    pravni_formy = """ CREATE INDEX "index pravni_formy" ON "pravni_formy" (
	"pravni_forma"
); """
    relevant_indices.append(pravni_formy)
#     pravni_formy_relation1 = """ CREATE INDEX "index pravni_formy_relation1" ON "pravni_formy_relation" (
# 	"company_id"
# ); """

#     pravni_formy_relation2 = """ CREATE INDEX "index pravni_formy_relation2" ON "pravni_formy_relation" (
# 	"id"
# ); """

#     pravnicke_osoby1 = """ CREATE INDEX "pravnicke_osoby1" ON "pravnicke_osoby" (
# 	"ico"
# ); """

#     pravnicke_osoby2 = """ CREATE INDEX "pravnicke_osoby2" ON "pravnicke_osoby" (
# 	"id"
# ); """

#     pravnicke_osoby3 = """ CREATE INDEX "pravnicke_osoby3" ON "pravnicke_osoby" (
# 	"reg_cislo"
# ); """

#     pravnicke_osoby4 = """ CREATE INDEX "pravnicke_osoby4" ON "pravnicke_osoby" (
# 	"nazev"
# ); """

#     predmety_cinnosti_relation1 = """ CREATE INDEX "index predmety cinnosti relation1" ON "predmety_cinnosti_relation" (
# 	"company_id"
# ); """

#     predmety_cinnosti_relation2 = """ CREATE INDEX "index predmety cinnosti relation2" ON "predmety_cinnosti_relation" (
# 	"id"
# ); """

#     predmety_cinnosti_relation3 = """ CREATE INDEX "index predmety cinnosti relation3" ON "predmety_cinnosti_relation" (
# 	"predmet_cinnosti_id"
# ); """

#     predmety_podnikani_relation1 = """ CREATE INDEX "index predmety podnikani relation1" ON "predmety_podnikani_relation" (
# 	"company_id"
# ); """

#     predmety_podnikani_relation2 = """ CREATE INDEX "index predmety podnikani relation2" ON "predmety_podnikani_relation" (
# 	"id"
# ); """

#     predmety_podnikani_relation3 = """ CREATE INDEX "index predmety podnikani relation3" ON "predmety_podnikani_relation" (
# 	"predmet_podnikani_id"
# ); """

    predmety_cinnosti1 = """ CREATE INDEX "index predmety_cinnosti1" ON "predmety_cinnosti" (
	"predmet_cinnosti"
); """
    relevant_indices.append(predmety_cinnosti1)
#     predmety_cinnosti2 = """ CREATE INDEX "index predmety_cinnosti2" ON "predmety_cinnosti" (
# 	"id"
# ); """

    predmety_podnikani1 = """ CREATE INDEX "index predmety_podnikani1" ON "predmety_podnikani" (
	"predmet_podnikani"
); """
    relevant_indices.append(predmety_podnikani1)
#     predmety_podnikani2 = """ CREATE INDEX "index predmety_podnikani2" ON "predmety_podnikani" (
# 	"id"
# ); """

#     prokuriste1 = """ CREATE INDEX "index prokuriste1" ON "prokuriste" (
# 	"id"
# ); """

#     prokuriste2 = """ CREATE INDEX "index prokuriste2" ON "prokuriste" (
# 	"company_id"
# ); """

#     prokuriste3 = """ CREATE INDEX "index prokuriste3" ON "prokuriste" (
# 	"prokurista_fo_id"
# ); """

#     prokuriste4 = """ CREATE INDEX "index prokuriste4" ON "prokuriste" (
# 	"adresa_id"
# ); """

#     sidlo_relation1 = """ CREATE INDEX "index sidlo relation1" ON "sidlo_relation" (
# 	"id"
# ); """

#     sidlo_relation_2 = """ CREATE INDEX "index sidlo relation2" ON "sidlo_relation" (
# 	"company_id"
# ); """

#     sidlo_relation_3 = """ CREATE INDEX "index sidlo relation3" ON "sidlo_relation" (
# 	"sidlo_id"
# ); """

#     soudni_zapis1 = """ CREATE INDEX "index soudni_zapis1" ON "zapis_soudy" (
# 	"company_id"
# ); """

#     soudni_zapis2 = """ CREATE INDEX "index soudni_zapis2" ON "zapis_soudy" (
# 	"id"
# ); """

#     spolecnici1 = """ CREATE INDEX "index spolecnici1" ON "spolecnici" (
# 	"id"
# ); """

    spolecnici2 = """ CREATE INDEX "index spolecnici2" ON "spolecnici" (
	"company_id"
); """
    relevant_indices.append(spolecnici2)

    spolecnici3 = """ CREATE INDEX "index spolecnici3" ON "spolecnici" (
	"spolecnik_fo_id"
); """
    relevant_indices.append(spolecnici3)

    spolecnici4 = """ CREATE INDEX "index spolecnici4" ON "spolecnici" (
	"spolecnik_po_id"
); """
    relevant_indices.append(spolecnici4)

    spolecnici5 = """ CREATE INDEX "index spolecnici5" ON "spolecnici" (
	"adresa_id"
); """
    relevant_indices.append(spolecnici5)

#     spolecnici_uvolneny_podil1 = """ CREATE INDEX "index uvolneny_podil1" on "spolecnici_uvolneny_podil" (
# 	"id"
# ); """

    spolecnici_uvolneny_podil2 = """ CREATE INDEX "index uvolneny_podil2" on "spolecnici_uvolneny_podil" (
	"company_id"
); """
    relevant_indices.append(spolecnici_uvolneny_podil2)

    spolecnici_spolecny_podil1 = """ CREATE INDEX "index spolecny_podil1" on "spolecnici_spolecny_podil" (
	"id"
); """
    relevant_indices.append(spolecnici_spolecny_podil1)

    spolecnici_spolecny_podil2 = """ CREATE INDEX "index spolecny_podil2" on "spolecnici_spolecny_podil" (
	"company_id"
); """
    relevant_indices.append(spolecnici_spolecny_podil2)

    statutarni_organy = """ CREATE INDEX "index statutarn_organy" ON "statutarni_organy" (
	"id",
	"statutarni_organ_text"
); """
    relevant_indices.append(statutarni_organy)
#     statutarni_organy_relation1 = """ CREATE INDEX "index statutarni organ relation1" ON "statutarni_organ_relation" (
# 	"id"
# ); """

#     statutarni_organy_relation2 = """ CREATE INDEX "index statutarni organ relation2" ON "statutarni_organ_clen_relation" (
# 	"statutarni_organ_id"
# ); """

    statutarni_organy_relation_3 = """ CREATE INDEX "index statutarni organ relation3" ON "statutarni_organ_relation" (
	"company_id"
); """
    relevant_indices.append(statutarni_organy_relation_3)

#     ubo1 = """ CREATE INDEX "index ubo1" ON "ubo" (
# 	"id"
# ); """

#     ubo2 = """ CREATE INDEX "index ubo2" ON "ubo" (
# 	"company_id"
# ); """

#     ubo3 = """ CREATE INDEX "index ubo3" ON "ubo" (
# 	"ubo_id"
# ); """

#     ubo4 = """ CREATE INDEX "index ubo4" ON "ubo" (
# 	"adresa_id"
# ); """

    ucel1 = """ CREATE INDEX "index ucel1" ON "ucel" (
	"ucel"
); """
    relevant_indices.append(ucel1)

#     ucel2 = """ CREATE INDEX "index ucel2" ON "predmety_podnikani" (
# 	"id"
# ); """

    ucel_relation1 = """ CREATE INDEX "index ucel relation1" ON "ucel_relation" (
	"company_id"
); """
    relevant_indices.append(ucel_relation1)
#     ucel_relation2 = """ CREATE INDEX "index ucel relation2" ON "ucel_relation" (
# 	"id"
# ); """

    ucel_relation3 = """ CREATE INDEX "index ucel relation3" ON "ucel_relation" (
	"ucel_id"
); """
    relevant_indices.append(ucel_relation3)
#     zakladni_kapital1 = """ CREATE INDEX "index zakladni kapital1" ON "zakladni_kapital" (
# 	"company_id"
# ); """

#     zakladni_kapital2 = """ CREATE INDEX "index zakladni kapital2" ON "zakladni_kapital" (
# 	"id"
# ); """
	
#     zpusob_jednani = """ CREATE INDEX "index zpusob_jednani" ON "zpusoby_jednani" (
# 	"id"
# ); """

#     zpusob_jednani_relation1 = """ CREATE INDEX "index zpusob_jednani_relation" ON "zpusoby_jednani_relation" (
# 	"id"
# ); """

#     zpusob_jednani_relation2 = """ CREATE INDEX "index zpusob jednani relation2" ON "zpusoby_jednani_relation" (
# 	"statutarni_organ_id"
# ); """

#     zpusob_jednani_relation3 = """ CREATE INDEX "index zpusob jednani relation3" ON "zpusoby_jednani_relation" (
# 	"zpusob_jednani_id"
# ); """

#     fyzicke_osoby1 = """ CREATE INDEX fyzicke_osoby1 ON fyzicke_osoby (
# 	datum_naroz 
# ); """

#     fyzicke_osoby2 = """ CREATE INDEX fyzicke_osoby2 ON fyzicke_osoby (
# 	jmeno
# ); """

#     fyzicke_osoby3 = """ CREATE INDEX fyzicke_osoby3 ON fyzicke_osoby (
# 	prijmeni
# ); """

#     fyzicke_osoby4 = """ CREATE INDEX fyzicke_osoby4 ON fyzicke_osoby (
# 	titul_pred
# ); """

#     fyzicke_osoby5 = """ CREATE INDEX fyzicke_osoby5 ON fyzicke_osoby (
# 	titul_za
# ); """

#     statutarni_organy_relation_4 = """ CREATE INDEX "index statutarni organ relation 4" ON "statutarni_organ_clen_relation" (
# 	"osoba_id"
# ); """

#     statutarni_organy_relation_5 = """ CREATE INDEX "index statutarni organ relation 5" ON "statutarni_organ_clen_relation" (
# 	"prav_osoba_id"
# ); """

    dr_relation_3 = """ CREATE INDEX "index dr clen relation3" ON "dr_organ_clen_relation" (
	"osoba_id"
); """
    relevant_indices.append(dr_relation_3)
    dr_relation_4 = """ CREATE INDEX "index dr clen relation4" ON "dr_organ_clen_relation" (
	"pravnicka_osoba_id"
); """
    relevant_indices.append(dr_relation_4)
#     akcionari3 = """ CREATE INDEX "index akcionari3" ON "jediny_akcionar" (
# 	"akcionar_fo_id"
# ); """

    # list_of_indices = [companies1, companies2, companies3, companies4, companies5, adresy1, adresy2, adresy3,
	# akcie, akcie2, akcionari1, akcionari2, akcionari3, dr_clen_relation1, dr_clen_relation2, dr_relation, dr_relation2, dr_relation_3, dr_relation_4, 
	# insolvency1, insolvency2, konkurz1, konkurz2, nazvy1, nazvy2, nazvy3, ostatni_skutecnosti, ostatni_skutecnosti2, 
	# pocty_clenu_organ1, pocty_clenu_organ2, podily1, podily2, podily3, podily4, podilnici1, podilnici2, podilnici3, podilnici4, podilnici5,
	# pravni_formy, pravni_formy_relation1, pravni_formy_relation2, 
	# predmety_cinnosti_relation1, predmety_cinnosti_relation2, predmety_cinnosti_relation3, predmety_podnikani_relation1, predmety_podnikani_relation2, 
	# predmety_podnikani_relation3, predmety_cinnosti1, predmety_cinnosti2, predmety_podnikani1, predmety_podnikani2, prokuriste1, 
	# prokuriste2, prokuriste3, prokuriste4, sidlo_relation1, sidlo_relation_2, sidlo_relation_3, soudni_zapis1, soudni_zapis2, spolecnici1, 
	# spolecnici2, spolecnici3, spolecnici4, spolecnici5, spolecnici_uvolneny_podil1, spolecnici_uvolneny_podil2, spolecnici_spolecny_podil1, spolecnici_spolecny_podil2, statutarni_organy, statutarni_organy_relation1, statutarni_organy_relation2, 
	# statutarni_organy_relation_3, statutarni_organy_relation_4, zakladni_kapital1, zakladni_kapital2, zpusob_jednani, zpusob_jednani_relation1, zpusob_jednani_relation2, 
	# zpusob_jednani_relation3, pravnicke_osoby1, pravnicke_osoby2, pravnicke_osoby3, pravnicke_osoby4, statutarni_organy_relation_5, fyzicke_osoby1, fyzicke_osoby2, fyzicke_osoby3, fyzicke_osoby4, fyzicke_osoby5, ubo1, ubo2, ubo3, ubo4, ucel1, ucel2, ucel_relation1, ucel_relation2, ucel_relation3]

    # list_of_indices = [companies2, companies3, companies4, companies5, adresy2, adresy3,
    # adresy4, adresy5, adresy6, adresy7, adresy8, adresy9, adresy10, adresy11, adresy12,  
	# akcie2, akcionari2, akcionari3, dr_clen_relation1, dr_relation2, dr_relation_3, dr_relation_4, 
	# insolvency2, konkurz1, nazvy1, nazvy2, ostatni_skutecnosti, 
	# pocty_clenu_organ1, podily2, podily3, podily4, podilnici2, podilnici3, podilnici4, podilnici5,
	# pravni_formy, pravni_formy_relation1, pravni_formy_relation2, 
	# predmety_cinnosti_relation1, predmety_cinnosti_relation3, predmety_podnikani_relation1,  
	# predmety_podnikani_relation3, predmety_cinnosti1, predmety_podnikani1,   
	# prokuriste2, prokuriste3, prokuriste4, sidlo_relation_2, sidlo_relation_3, soudni_zapis1,  
	# spolecnici2, spolecnici3, spolecnici4, spolecnici5, spolecnici_uvolneny_podil2, spolecnici_spolecny_podil2, statutarni_organy, statutarni_organy_relation2, 
	# statutarni_organy_relation_3, statutarni_organy_relation_4, zakladni_kapital1, zpusob_jednani_relation2, 
	# zpusob_jednani_relation3, pravnicke_osoby1, pravnicke_osoby3, pravnicke_osoby4, statutarni_organy_relation_5, fyzicke_osoby1, fyzicke_osoby2, fyzicke_osoby3, fyzicke_osoby4, fyzicke_osoby5, ubo2, ubo3, ubo4, ucel1, ucel_relation1, ucel_relation3]
    i = 0
    for elem in relevant_indices:
        i += 1
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(i)
            print(e)