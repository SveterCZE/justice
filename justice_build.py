from db_creation import create_DB
from download_files import download_data, get_valid_filenames, download_criminal_records
from update_db import update_DB
from backup_DB import backup_DB
from insert_criminal_records import insert_criminal_records
from app import return_conn
import os

def main():
    # valid_files = []
    # DB_name = "justice.db"
    # backup_DB()
    # create_DB(DB_name)
    # Download commercial register data
    # valid_files = get_valid_filenames()
    # os.makedirs("data", exist_ok=True)
    # for valid_file in valid_files:
        # download_data(valid_file)
    # for valid_file in valid_files:
        # modified_file_name = os.path.join(str(os.getcwd()), "data", valid_file + ".xml")
    conn = return_conn()
    cur = conn.cursor()
    cur.execute('select \'drop table "\' || tablename || \'" cascade;\' from pg_tables where schemaname = \'public\';')
    instructions = cur.fetchall()
    for elem in instructions:
        print(elem)
        cur.execute(elem[0])
    # cur.execute('DROP TABLE IF EXISTS companies CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS pravni_formy CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS pravni_formy_relation CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS zapis_soudy CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS adresy_v2 CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS sidlo_relation CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS nazvy CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS insolvency_events CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS konkurz_events CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS statutarni_organy CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS statutarni_organ_relation CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS pocty_clenu_organu CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS zpusoby_jednani CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS zpusoby_jednani_relation CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS statutarni_organ_clen_relation CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS fyzicke_osoby CASCADE;')
    # cur.execute('DROP TABLE IF EXISTS pravnicke_osoby CASCADE;')
    conn.commit()
    # create_DB(conn)
    # update_DB("as-full-ostrava-2023.xml", conn)
    # Download criminal records
    # download_criminal_records()
    # insert_criminal_records(DB_name)

main()