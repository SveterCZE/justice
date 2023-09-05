import sqlite3
from app import return_conn
import xml.etree.ElementTree as ET
import os
from update_db import get_primary_sql_key

def insert_criminal_records():
    print("Inserting the criminal register information")
    conn = return_conn()
    c = conn.cursor()
    file_address = os.path.join(str(os.getcwd()), "data", "criminal_records.xml")
    tree = ET.parse(file_address)
    root = tree.getroot()
    for child in root:
        process_individual_extracts(child, c)
    conn.commit()
    conn.close()
    return
    
def process_individual_extracts(extract, c):
    ICO = get_ICO(extract)
    if ICO == -1:
        return
    else:
        court_records = find_court_records(extract)
        relevant_paragraphs = find_relevant_paragraphs(extract)
        penalties = find_penalties(extract)
        primary_sql_key = get_primary_sql_key(c, ICO)
        if primary_sql_key != False:
            insert_crimnal_data_to_DB(c, primary_sql_key, court_records, relevant_paragraphs, penalties)
    return

def get_ICO(extract):
    person_entry = extract[0][0][2]
    temp_ico = person_entry.text
    if temp_ico.isnumeric() == True:
        return temp_ico
    else:
        return -1

def find_court_records(extract):
    # TODO --- Make sure that the records are extracted correctly based on the tags
    court_records = []
    court_records_rider = extract[1][0][0]
    for child in court_records_rider:
        if "spisZnacka" in child.tag:
            court_records.append(child.text)
        if "organizace" in child.tag:
            court_records.append(child.text)
        if "odvolaci" in child.tag:
            for sub_child in child:
                if "spisZnacka" in sub_child.tag:
                    court_records.append(sub_child.text)
                if "organizace" in sub_child.tag:
                    court_records.append(sub_child.text)
    return court_records

def find_relevant_paragraphs(extract):
    paragraphs = []
    paragraphs_rider = extract[1][0][1]
    for individual_paragraph in paragraphs_rider:
        paragraphs.append(extract_paragraph_info(individual_paragraph))
    return paragraphs

def extract_paragraph_info(individual_paragraph):
    text_description = "§"
    for child in individual_paragraph[0]:
        if "Cislo" in child.tag:
            text_description += child.text
        if "Pismeno" in child.tag:
            text_description += ", odst. "
            text_description += child.text
        if "zakon" in child.tag:
            temp_law_description = child.text
            # temp_law_description[0].tolower()
            text_description += ", "
            text_description += temp_law_description
    return text_description

def find_penalties(extract):
    paragraphs_rider = extract[1][0]
    for child in paragraphs_rider:
        if "tresty" in child.tag:
            return extract_penalties_info(child)

def extract_penalties_info(extract):
    penalties = []
    for child in extract:
        if "druh" in child[0].tag:
            penalties.append(child[0].text)
    return penalties

def insert_crimnal_data_to_DB(c, primary_sql_key, court_records, relevant_paragraphs, penalties):
    first_instance = court_records[1] + ", sp. zn. " + court_records[0]
    if len(court_records) > 2:
        second_instance = court_records[3] + ", sp. zn. " + court_records[2]
    else:
        second_instance = None
    text_paragraphs = ""
    if relevant_paragraphs != None:
        for elem in relevant_paragraphs:
            text_paragraphs += elem
            text_paragraphs += ", "
    text_penalties = ""
    if penalties != None:
        for elem in penalties:
            text_penalties += elem
            text_penalties += ", "
    c.execute("INSERT INTO criminal_records (company_id, first_instance, second_instance, paragraphs, penalties) VALUES (%s, %s, %s, %s, %s)", (primary_sql_key, first_instance, second_instance, text_paragraphs[:-2], text_penalties[:-2],))
    return 0