from datetime import datetime
import os
import requests
import gzip
import shutil
import send2trash
from lxml import etree

def download_data(typy_po, soudy):
    rok = str(datetime.now().year)
    for osoba in typy_po:
        for soud in soudy:
            update_data(osoba + "-full-" + soud + "-" + rok + ".xml.gz")

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