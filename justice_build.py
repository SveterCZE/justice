from db_creation import create_DB
from download_files import download_data, get_valid_filenames, download_criminal_records
from update_db import update_DB
from backup_DB import backup_DB
from insert_criminal_records import insert_criminal_records
import os

def main():
    DB_name = "justice.db"
    backup_DB()
    create_DB(DB_name)
    # Download commercial register data
    valid_files = get_valid_filenames()
    os.makedirs("data", exist_ok=True)
    for valid_file in valid_files:
        download_data(valid_file)
    for valid_file in valid_files:
        modified_file_name = os.path.join(str(os.getcwd()), "data", valid_file + ".xml")
        update_DB(modified_file_name, DB_name)
    # Download criminal records
    download_criminal_records()
    insert_criminal_records(DB_name)

main()