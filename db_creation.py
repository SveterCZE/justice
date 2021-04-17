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
	"oddil"	TEXT,
	"vlozka"	TEXT,
	"soud"	TEXT,
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

    ucel = """ CREATE TABLE "ucel" (
	"id"	INTEGER NOT NULL,
	"ucel"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
); """

    ucel_relation = """ CREATE TABLE "ucel_relation" (
	"id"	INTEGER NOT NULL UNIQUE,
	"company_id"	INTEGER NOT NULL,
	"ucel_id"	INTEGER NOT NULL,
	"zapis_datum"	DATE,
	"vymaz_datum"	DATE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "companies"("id"),
	FOREIGN KEY("ucel_id") REFERENCES "ucel"("id")
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

    list_of_tables = [companies, adresy_v2, akcie, dr_relation, dr_organ_clen_relation, druhy_podilu, fyzicke_osoby, insolvency_events, 
    jediny_akcionar, konkurz_events, nazvy, ostatni_skutecnosti, pocty_clenu_DR, pocty_clenu_organu, podily, pravni_formy, 
    pravni_formy_relation, pravnicke_osoby, predmety_cinnosti, predmety_cinnosti_relation, prdmety_podnikani, predmety_podnikani_relation,
    prokura_common_texts, prokuriste, sidlo_relation, spolecnici, statutarni_organ_clen_relation, statutarni_organ_relation, statutarni_organy, 
    ucel, ucel_relation, zakladni_kapital, zapis_soudy, zpusoby_jednani, zpusoby_jednani_relation]
    for elem in list_of_tables:
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(e)

def create_indices(conn):
    companies1 = """ CREATE INDEX "index companies1" ON "companies" (
	"id"
); """

    companies2 = """ CREATE INDEX "index companies2" ON "companies" (
	"ico"
); """

    companies3 = """ CREATE INDEX "index companies3" ON "companies" (
	"nazev"
); """

    companies4 = """ CREATE INDEX "index companies4" ON "companies" (
	"oddil"
); """

    companies5 = """ CREATE INDEX "index companies5" ON "companies" (
	"vlozka"
); """

    adresy1 = """ CREATE INDEX "index adresy1" ON "adresy_v2" (
	"id"
); """

    adresy2 = """ CREATE INDEX "index adresy2" ON "adresy_v2" (
	"obec"
); """

    adresy3 = """ CREATE INDEX "index adresy3" ON "adresy_v2" (
	"ulice"
); """

    akcie = """ CREATE INDEX "index akcie1" ON "akcie" (
	"id"
); """

    akcie2 = """ CREATE INDEX "index akcie2" ON "akcie" (
	"company_id"
); """

    akcionari1 = """ CREATE INDEX "index akcionari1" ON "jediny_akcionar" (
	"id"
); """

    akcionari2 = """ CREATE INDEX "index akcionari2" ON "jediny_akcionar" (
	"company_id"
); """

    dr_clen_relation1 = """ CREATE INDEX "index dr clen relation1" ON "dr_organ_clen_relation" (
	"dozorci_rada_id"
); """

    dr_clen_relation2 = """ CREATE INDEX "index dr clen relation2" ON "dr_organ_clen_relation" (
	"id"
); """

    dr_relation = """ CREATE INDEX "index dr relation1" ON "dozorci_rada_relation" (
	"id"
); """

    dr_relation2 = """ CREATE INDEX "index dr relation2" ON "dozorci_rada_relation" (
	"company_id"
); """

    insolvency1 = """ CREATE INDEX "index insolvency1" ON "insolvency_events" (
	"id"
); """

    insolvency2 = """ CREATE INDEX "index insolvency2" ON "insolvency_events" (
	"company_id"
); """

    konkurz1 = """CREATE INDEX "index konkurz1" ON "konkurz_events" (
	"company_id"
); """

    konkurz2 = """CREATE INDEX "index konkurz2" ON "konkurz_events" (
	"id"
); """

    nazvy1 = """ CREATE INDEX "index nazvy1" ON "nazvy" (
	"nazev_text"
); """

    nazvy2 = """ CREATE INDEX "index nazvy2" ON "nazvy" (
	"company_id"
); """

    nazvy3 = """ CREATE INDEX "index nazvy3" ON "nazvy" (
	"id"
); """

    ostatni_skutecnosti = """ CREATE INDEX "index ostatni skutecnosti1" ON "ostatni_skutecnosti" (
	"company_id"
); """

    ostatni_skutecnosti2 = """ CREATE INDEX "index ostatni skutecnosti2" ON "ostatni_skutecnosti" (
	"id"
); """

    pocty_clenu_organ1 = """ CREATE INDEX "index pocty clenu org1" ON "pocty_clenu_organu" (
	"organ_id"
); """

    pocty_clenu_organ2 = """ CREATE INDEX "index pocty clenu org2" ON "pocty_clenu_organu" (
	"id"
); """

    podily1 = """ CREATE INDEX "index podily1" ON "podily" (
	"id"
); """

    podily2 = """ CREATE INDEX "index podily2" ON "podily" (
	"spolecnik_id"
); """

    pravni_formy = """ CREATE INDEX "index pravni_formy" ON "pravni_formy" (
	"pravni_forma"
); """

    pravni_formy_relation1 = """ CREATE INDEX "index pravni_formy_relation1" ON "pravni_formy_relation" (
	"company_id"
); """

    pravni_formy_relation2 = """ CREATE INDEX "index pravni_formy_relation2" ON "pravni_formy_relation" (
	"id"
); """

    pravnicke_osoby1 = """ CREATE INDEX "pravnicke_osoby1" ON "pravnicke_osoby" (
	"ico"
); """

    pravnicke_osoby2 = """ CREATE INDEX "pravnicke_osoby2" ON "pravnicke_osoby" (
	"id"
); """

    pravnicke_osoby3 = """ CREATE INDEX "pravnicke_osoby3" ON "pravnicke_osoby" (
	"reg_cislo"
); """

    pravnicke_osoby4 = """ CREATE INDEX "pravnicke_osoby4" ON "pravnicke_osoby" (
	"nazev"
); """

    predmety_cinnosti_relation1 = """ CREATE INDEX "index predmety cinnosti relation1" ON "predmety_cinnosti_relation" (
	"company_id"
); """

    predmety_cinnosti_relation2 = """ CREATE INDEX "index predmety cinnosti relation2" ON "predmety_cinnosti_relation" (
	"id"
); """

    predmety_cinnosti_relation3 = """ CREATE INDEX "index predmety cinnosti relation3" ON "predmety_cinnosti_relation" (
	"predmet_cinnosti_id"
); """

    predmety_podnikani_relation1 = """ CREATE INDEX "index predmety podnikani relation1" ON "predmety_podnikani_relation" (
	"company_id"
); """

    predmety_podnikani_relation2 = """ CREATE INDEX "index predmety podnikani relation2" ON "predmety_podnikani_relation" (
	"id"
); """

    predmety_podnikani_relation3 = """ CREATE INDEX "index predmety podnikani relation3" ON "predmety_podnikani_relation" (
	"prdemet_podnikani_id"
); """

    predmety_cinnosti1 = """ CREATE INDEX "index predmety_cinnosti1" ON "predmety_cinnosti" (
	"predmet_cinnosti"
); """

    predmety_cinnosti2 = """ CREATE INDEX "index predmety_cinnosti2" ON "predmety_cinnosti" (
	"id"
); """

    predmety_podnikani1 = """ CREATE INDEX "index predmety_podnikani1" ON "predmety_podnikani" (
	"predmet_podnikani"
); """

    predmety_podnikani2 = """ CREATE INDEX "index predmety_podnikani2" ON "predmety_podnikani" (
	"id"
); """

    prokuriste1 = """ CREATE INDEX "index prokuriste1" ON "prokuriste" (
	"id"
); """

    prokuriste2 = """ CREATE INDEX "index prokuriste2" ON "prokuriste" (
	"company_id"
); """

    prokuriste3 = """ CREATE INDEX "index prokuriste3" ON "prokuriste" (
	"prokurista_fo_id"
); """

    prokuriste4 = """ CREATE INDEX "index prokuriste4" ON "prokuriste" (
	"adresa_id"
); """

    sidlo_relation1 = """ CREATE INDEX "index sidlo relation1" ON "sidlo_relation" (
	"id"
); """

    sidlo_relation_2 = """ CREATE INDEX "index sidlo relation2" ON "sidlo_relation" (
	"company_id"
); """

    sidlo_relation_3 = """ CREATE INDEX "index sidlo relation3" ON "sidlo_relation" (
	"sidlo_id"
); """

    soudni_zapis1 = """ CREATE INDEX "index soudni_zapis1" ON "zapis_soudy" (
	"company_id"
); """

    soudni_zapis2 = """ CREATE INDEX "index soudni_zapis2" ON "zapis_soudy" (
	"id"
); """

    spolecnici1 = """ CREATE INDEX "index spolecnici1" ON "spolecnici" (
	"id"
); """

    spolecnici2 = """ CREATE INDEX "index spolecnici2" ON "spolecnici" (
	"company_id"
); """

    spolecnici3 = """ CREATE INDEX "index spolecnici3" ON "spolecnici" (
	"spolecnik_fo_id"
); """

    spolecnici4 = """ CREATE INDEX "index spolecnici4" ON "spolecnici" (
	"spolecnik_po_id"
); """

    spolecnici5 = """ CREATE INDEX "index spolecnici5" ON "spolecnici" (
	"adresa_id"
); """

    statutarni_organy = """ CREATE INDEX "index statutarn_organy" ON "statutarni_organy" (
	"id",
	"statutarni_organ_text"
); """

    statutarni_organy_relation1 = """ CREATE INDEX "index statutarni organ relation1" ON "statutarni_organ_relation" (
	"id"
); """

    statutarni_organy_relation2 = """ CREATE INDEX "index statutarni organ relation2" ON "statutarni_organ_clen_relation" (
	"statutarni_organ_id"
); """

    statutarni_organy_relation_3 = """ CREATE INDEX "index statutarni organ relation 3" ON "statutarni_organ_relation" (
	"company_id"
); """

    ucel1 = """ CREATE INDEX "index ucel1" ON "ucel" (
	"ucel"
); """

    ucel2 = """ CREATE INDEX "index ucel2" ON "predmety_podnikani" (
	"id"
); """

    ucel_relation1 = """ CREATE INDEX "index ucel relation1" ON "ucel_relation" (
	"company_id"
); """

    ucel_relation2 = """ CREATE INDEX "index ucel relation2" ON "ucel_relation" (
	"id"
); """

    ucel_relation3 = """ CREATE INDEX "index ucel relation3" ON "ucel_relation" (
	"ucel_id"
); """

    zakladni_kapital1 = """ CREATE INDEX "index zakladni kapital1" ON "zakladni_kapital" (
	"company_id"
); """

    zakladni_kapital2 = """ CREATE INDEX "index zakladni kapital2" ON "zakladni_kapital" (
	"id"
); """
	
    zpusob_jednani = """ CREATE INDEX "index zpusob_jednani" ON "zpusoby_jednani" (
	"id"
); """

    zpusob_jednani_relation1 = """ CREATE INDEX "index zpusob_jednani_relation" ON "zpusoby_jednani_relation" (
	"id"
); """

    zpusob_jednani_relation2 = """ CREATE INDEX "index zpusob jednani relation2" ON "zpusoby_jednani_relation" (
	"statutarni_organ_id"
); """

    zpusob_jednani_relation3 = """ CREATE INDEX "index zpusob jednani relation3" ON "zpusoby_jednani_relation" (
	"zpusob_jednani_id"
); """

    fyzicke_osoby1 = """ CREATE INDEX "index fyzicke_osoby1" ON "fyzicke_osoby" (
	"id"
); """

	statutarni_organy_relation_4 = """ CREATE INDEX "index statutarni organ relation 4" ON "statutarni_organ_clen_relation" (
	"osoba_id"
); """

	dr_relation_3 = """ CREATE INDEX "index dr clen relation3" ON "dr_organ_clen_relation" (
	"osoba_id"
); """

	akcionari3 = """ CREATE INDEX "index akcionari3" ON "jediny_akcionar" (
	"akcionar_fo_id"
); """

    list_of_indices = [companies1, companies2, companies3, companies4, companies5, adresy1, adresy2, adresy3,
	akcie, akcie2, akcionari1, akcionari2, akcionari3, dr_clen_relation1, dr_clen_relation2, dr_relation, dr_relation2, dr_relation_3, 
	insolvency1, insolvency2, konkurz1, konkurz2, nazvy1, nazvy2, nazvy3, ostatni_skutecnosti, ostatni_skutecnosti2, 
	pocty_clenu_organ1, pocty_clenu_organ2, podily1, podily2, pravni_formy, pravni_formy_relation1, pravni_formy_relation2, 
	predmety_cinnosti_relation1, predmety_cinnosti_relation2, predmety_cinnosti_relation3, predmety_podnikani_relation1, predmety_podnikani_relation2, 
	predmety_podnikani_relation3, predmety_cinnosti1, predmety_cinnosti2, predmety_podnikani1, predmety_podnikani2, prokuriste1, 
	prokuriste2, prokuriste3, prokuriste4, sidlo_relation1, sidlo_relation_2, sidlo_relation_3, soudni_zapis1, soudni_zapis2, spolecnici1, 
	spolecnici2, spolecnici3, spolecnici4, spolecnici5, statutarni_organy, statutarni_organy_relation1, statutarni_organy_relation2, 
	statutarni_organy_relation_3, statutarni_organy_relation_4, zakladni_kapital1, zakladni_kapital2, zpusob_jednani, zpusob_jednani_relation1, zpusob_jednani_relation2, 
	zpusob_jednani_relation3, pravnicke_osoby1, pravnicke_osoby2, pravnicke_osoby3, pravnicke_osoby4, fyzicke_osoby1, ucel1, ucel2, ucel_relation1, ucel_relation2, ucel_relation3]
    i = 0
    for elem in list_of_indices:
        i += 1
        try:
            c = conn.cursor()
            c.execute(elem)
        except Exception as e:
            print(i)
            print(e)