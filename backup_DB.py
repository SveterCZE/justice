import shutil
import os

def backup_DB():
    os.makedirs("backup", exist_ok=True)
    shutil.move("justice.db", "backup/justice.db")
