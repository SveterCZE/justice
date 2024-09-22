from datetime import datetime
import os
import requests
import gzip
import shutil
import send2trash
from lxml import etree


def get_valid_filenames():
    FILENAME = "justice_files.txt"
    my_file = download_list_filenames()
    save_file(my_file, FILENAME)
    valid_files = get_files_list(FILENAME)
    return valid_files   

def download_list_filenames():
    source = "https://dataor.justice.cz/api/3/action/package_list"
    download = requests.get(source, stream = True)
    try:
        print("Downloading file ", source)
        download.raise_for_status()
    except Exception as exc:
        print("There was a problem: %s. Please check whether https://dataor.justice.cz is online. If not, try again later." % (exc))
        return None
    return download

def save_file(download, temp_file):
    temp_file = open(temp_file, "wb")
    for chunk in download.iter_content(1000):
        temp_file.write(chunk)
    temp_file.close()
    return 0

def get_files_list(my_file):
    f = open(my_file, "r")
    valid_files = []
    for line in f:
        l1 = line[1:-2].split("[")[1].split(",")
        for elem in l1:
            if is_valid_file(elem[1:-1]) == True:
                valid_files.append(elem[1:-1])
    valid_files.sort()
    return valid_files

def is_valid_file(tested_file):    
    if tested_file.split("-")[1] == "full" and tested_file.split("-")[3] == str(datetime.now().year):
        return True
    else:
        return False

def download_data(filename):
    source = "https://dataor.justice.cz/api/file/" + filename + ".xml.gz"
    # temp_file = "D:\\Programovani\\Moje vymysly\\Justice\\data\\temp-" + filename
    temp_file = os.path.join(str(os.getcwd()), "data", "temp-" + filename + ".xml.gz")
    # temp_file = str(os.getcwd()) + "\\data\\temp-" + filename
    downloaded_OR = downloadOR(source)
    if downloaded_OR != None:
        save_temp_file(downloaded_OR, temp_file)
        unzip_file(filename, temp_file)
        delete_archive(temp_file)
        # parse_check = parseOR(temp_file[:-3])
        # if parse_check == True:
        update_main_file(filename + ".xml", temp_file[:-3])
            # delete_archive(temp_file[:-3])
        # else:
        #     delete_archive(temp_file)
    return 0

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
    except Exception as f:
        print(f)
        return False
    return True

def save_temp_file(download, temp_file):
    temp_file = open(temp_file, "wb")
    for chunk in download.iter_content(1000000):
        temp_file.write(chunk)
    temp_file.close()
    return 0

def update_main_file(filename, temp_file):
    shutil.move(temp_file, os.path.join(str(os.getcwd()), "data", filename))
    return 0

def delete_temp_file(temp_file):
    temp_file = open(temp_file, "w")
    temp_file.write("0")
    temp_file.close()
    return 0

def unzip_file(filename, temp_file):
    with gzip.open(temp_file, 'rb') as f_in:
        with open(os.path.join(str(os.getcwd()), "data", "temp-" + filename + ".xml"), "wb") as f_out:
        # with open(str(os.getcwd()) + "\\data\\temp-" + filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return 0

def delete_archive(file):
    send2trash.send2trash(file)
    return 0

def download_criminal_records():
    source = "https://eservice-po.rejtr.justice.cz/public/odsouzeni_xml"
    file_address = os.path.join(str(os.getcwd()), "data", "criminal_records.xml")
    downloaded_criminal_extracts = downloadOR(source)
    if downloaded_criminal_extracts != None:
        save_temp_file(downloaded_criminal_extracts, file_address)
    return 0