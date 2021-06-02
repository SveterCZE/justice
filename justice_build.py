from db_creation import create_DB
from download_files import download_data, get_valid_filenames
from update_db import update_DB
import os

def main():
    DB_name = "justice.db"
    create_DB(DB_name)
    valid_files = get_valid_filenames()
    os.makedirs("data", exist_ok=True)
    for valid_file in valid_files:
        download_data(valid_file)
    for valid_file in valid_files:
        modified_file_name = os.path.join(str(os.getcwd()), "data", valid_file + ".xml")
        update_DB(modified_file_name, DB_name)
  
main()
