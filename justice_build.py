from db_creation import create_DB, create_indices
from download_files import download_data, get_valid_filenames, download_criminal_records
from update_db import update_DB
from backup_DB import backup_DB
from insert_criminal_records import insert_criminal_records
from app import return_conn
import os
import cProfile

def main():
    # Download commercial register data
    valid_files = get_valid_filenames()
    os.makedirs("data", exist_ok=True)
    for valid_file in valid_files:
        download_data(valid_file)
    # Connect to the database
    conn = return_conn()
    cur = conn.cursor()
    # Clean the existing database and initialise a new one
    cur.execute('select \'drop table "\' || tablename || \'" cascade;\' from pg_tables where schemaname = \'public\';')
    instructions = cur.fetchall()
    for elem in instructions:
        cur.execute(elem[0])
    conn.commit()
    create_DB(conn)
    create_indices(conn)
    # Insert data ffrom individual files
    for valid_file in valid_files:
        modified_file_name = os.path.join(str(os.getcwd()), "data", valid_file + ".xml")
        update_DB(modified_file_name, conn)
    # Download criminal records
    download_criminal_records()
    insert_criminal_records()

# main()
cProfile.run('main()')