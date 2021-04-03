import sqlite3

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
	FOREIGN KEY("sidlo_id") REFERENCES "adresy_v2"("id"),
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

	akcie2 = """ CREATE INDEX "index akcie 2" ON "akcie" (
	"company_id"
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

	nazvy2 = """ CREATE INDEX "index nazvy 2" ON "nazvy" (
	"company_id"
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

	pravni_formy_relation_2 = """ CREATE INDEX "index pravni_formy_relation_2" ON "pravni_formy_relation" (
	"company_id"
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

	sidlo_relation_2 = """ CREATE INDEX "index sidlo relation 2" ON "sidlo_relation" (
	"company_id"
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

	statutarni_organy_relation_3 = """ CREATE INDEX "index statutarni organ relation 3" ON "statutarni_organ_relation" (
	"company_id"
); """

    v2 = """ CREATE INDEX "index v2" ON "statutarni_organ_relation" (
	"statutarni_organ_id",
	"company_id",
	"id"
); """

    zakladni_kapital = """ CREATE INDEX "index zakladni kapital" ON "zakladni_kapital" (
	"company_id"
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

	zpusob_jednani_relation_2 = """ CREATE INDEX "index zpusob jednani relation 2" ON "zpusoby_jednani_relation" (
	"statutarni_organ_id"
); """

    zpusoby_jednani = """ CREATE INDEX "index zpusoby_jednani" ON "zpusoby_jednani" (
	"zpusob_jednani_text"
); """

    pravnicke_osoby_index = """ CREATE INDEX "pravnicke_osoby_index" ON "pravnicke_osoby" (
	"ico",
	"reg_cislo",
	"nazev"
); """

    list_of_indices = [companies, adresy, adresa_text, akcie, akcie2, akcionari, companies_ico, companies_nazvy, companies_vznik, dr_clen_relation, dr_relation, dr_relation2, insolvency_events, insolvency2, jmena_firem, nazvy_nazev_text, nazvy2, obce, obec_jmeno, osoby, ostatni_skutecnosti2, 
    pocty_clenu_organ, podily, podily_spolecnik, pravni_formy, pravni_formy_relation_2, predmety_cinnosti_relation_v2, predmety_podnikani_relation, predmety_cinnosti, predmety_podnikani, prokuriste, sidlo, sidlo_relation, sidlo_relation_2, sidlo2, soudni_zapis, spolecnici, spolecnici2, statutarni_organy, statutarni_organy_relation, 
    statutarni_organy_relation_v2, statutarni_organy_relation_3, v2, zakladni_kapital, zapis2, zapis_soudy, zpusob_jednani, zpusob_jednani_relation, zpusob_jednani_relation_2, zpusoby_jednani, pravnicke_osoby_index]
    for elem in list_of_indices:
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(e)