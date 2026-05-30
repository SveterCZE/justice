from datetime import datetime
import time
import os
import requests
import gzip
import shutil
import send2trash
import logging
from lxml import etree


def get_valid_filenames():
    FILENAME = "justice_files.txt"
    my_file = download_list_filenames()
    save_file(my_file, FILENAME)
    valid_files = get_files_list(FILENAME)
    return valid_files   

def download_list_filenames():
    logging.captureWarnings(True)
    source = "https://dataor.justice.cz/api/3/action/package_list"
    download = requests.get(source, stream = True, verify=False)
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

def download_and_save_file(source, temp_file_path, max_retries=100, delay_seconds=60):
    """
    Downloads and streams the file directly to the disk. 
    Catches connection drops mid-download and retries.
    """
    for attempt in range(max_retries):
        print(f"Downloading file {source} (Attempt {attempt + 1} of {max_retries})")
        
        try:
            # timeout=(15, 60): 15s to connect, 60s max wait between data chunks
            with requests.get(source, stream=True, verify=False, timeout=(15, 60)) as download:
                download.raise_for_status()
                
                # Write the file chunk by chunk inside the try block
                with open(temp_file_path, 'wb') as f:
                    for chunk in download.iter_content(chunk_size=1000000):
                        if chunk: 
                            f.write(chunk)
            
            # print(f"Successfully downloaded and saved to {temp_file_path}")
            return True # Success
            
        except requests.exceptions.RequestException as exc:
            print(f"Network error on attempt {attempt + 1}: {exc}")
            
            # Delete the corrupted/partial file before the next retry
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            if attempt < max_retries - 1:
                print(f"Waiting {delay_seconds} seconds before retrying...\n")
                time.sleep(delay_seconds)
            else:
                print(f"All {max_retries} retry attempts exhausted for {source}.")
                return False

def download_data(filename):
    source = "https://dataor.justice.cz/api/file/" + filename + ".xml.gz"
    temp_file = os.path.join(str(os.getcwd()), "data", "temp-" + filename + ".xml.gz")
    
    # Download and save the file in one go to catch streaming timeouts
    success = download_and_save_file(source, temp_file)
    
    if success:
        # Proceed with processing only if the download entirely succeeded
        unzip_file(filename, temp_file)
        delete_archive(temp_file)
        
        # temp_file[:-3] removes the '.gz' to get the unzipped xml file path
        unzipped_temp_file = temp_file[:-3]
        update_main_file(filename + ".xml", unzipped_temp_file)
        
    else:
        print(f"Skipping {filename} due to download failure.")
        
    return 0

def downloadOR(source):
    logging.captureWarnings(True)
    download = requests.get(source, stream = True,verify=False)
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

# def download_criminal_records():
#     source = "https://eservice-po.rejtr.justice.cz/public/odsouzeni_xml"
#     file_address = os.path.join(str(os.getcwd()), "data", "criminal_records.xml")
#     downloaded_criminal_extracts = downloadOR(source)
#     if downloaded_criminal_extracts != None:
#         save_temp_file(downloaded_criminal_extracts, file_address)
#     return 0