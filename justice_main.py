from db_creation import create_DB
from download_files import download_data
from update_db import update_DB

def main():
    typy_po = ["as", "sro", "vos", "ks", "dr", "zajzdrpo", "zahrfos", "ustav", "svj", "spolek", "prisp", "pobspolek",
                    "oszpo", "osznadf", "osznad", "orgzam", "odbororg", "nadf", "nad", "evrspol", "evrhzs", "evrdrspol"]
    soudy = ["praha", "plzen", "brno", "ceske_budejovice", "hradec_kralove", "ostrava", "usti_nad_labem"]
    DB_name = "justice.db"
    create_DB(DB_name)
    download_data(typy_po, soudy)
    update_DB(typy_po, soudy, DB_name)

main()