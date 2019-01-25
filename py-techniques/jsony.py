import json
import ijson
from random import choice
from collections import defaultdict
from datetime import datetime
import argparse
import os
import psutil

def parseJSON(filename=r"C:\Users\ricardogu\Desktop\test.json"):

    """ Using standard json library. Loads file into memory as a Python object tree.
    """
    created, process = datetime.now(), psutil.Process(os.getpid())
    mem_before = process.memory_info().rss/1024/1024 # bytes to MB

    try:

        with open(filename, "r", encoding="utf-8") as f:
            
            jsonObj = json.load(f) # throws JSONDecodeError

            server = jsonObj['server_db']
            servername = jsonObj['server_name']
            ultipro = jsonObj['ultipro']
            standalone = jsonObj['standalone']

            print(f'Processed {len(ultipro)} ultipro co, {len(standalone)} standalone co ({server}, {servername})')

    except Exception as e:
        print(e)

    mem_after = process.memory_info().rss/1024/1024 # bytes to MB
    elapsed = datetime.now() - created
    print(f'Parsed {filename} via inmemory\n elapsed: {elapsed}\n memory before: {mem_before}\n memory after: {mem_after}\n consumed: {mem_after - mem_before}')

def parseiJSON(filename=r"C:\Users\ricardogu\Desktop\test3.json"):

    """ Using ijson library allows streaming the json file.
    """
    created, process = datetime.now(), psutil.Process(os.getpid())
    mem_before = process.memory_info().rss/1024/1024 # bytes to MB

    try:

        server_name = server_db = None
        ultipro, standalone = [], []
        tmpCo = tmpAR = tmpEmpInfo = None

        # First, scan server metadata.
        with open(filename, "r", encoding="utf-8") as f:
            
            # Use this to get prefix for the json elements.
            parsed = ijson.parse(f) # returns iterator

            for pre, evt, val in parsed: # returns all (prefix, event, value)
                if (pre, evt) == ('server_db', 'string'):
                    server_db = val

                elif (pre, evt) == ('server_name', 'string'):
                    server_name = val

                if server_db and server_name:
                    break

        with open(filename, "r", encoding="utf-8") as f:
            
            # Use this to get prefix for the json elements.
            parsed = ijson.parse(f) # returns iterator

            for pre, evt, val in parsed: # returns all (prefix, event, value)
                if  (pre, evt) == ('ultipro.item.ar_number', 'string'):
                    ultipro.append(val)
                # New standalone co
                elif (pre, evt) == ('standalone.item', 'start_map'):
                    tmpEmpInfo = defaultdict(int)
                elif (pre, evt) == ('standalone.item.employee_info.item.location', 'string'):
                    tmpEmpInfo[val] += 1
                elif (pre, evt) == ('standalone.item.employee_info.item.location', 'null'):
                    # Default null to 'Unknown'
                    tmpEmpInfo['Unknown'] += 1
                elif (pre, evt) == ('standalone.item.company_name', 'string'):
                    tmpCo = val
                elif (pre, evt) == ('standalone.item.ar_number', 'string'):
                    tmpAR = val
                # End standalone co
                elif (pre, evt) == ('standalone.item', 'end_map'):
                    if tmpEmpInfo: # ignore N/A
                        standalone.append([tmpCo, tmpAR, tmpEmpInfo])

            print(f'Processed {len(ultipro)} ultipro co, {len(standalone)} standalone co ({server_db}, {server_name})')

    except Exception as e:
        print(e)

    mem_after = process.memory_info().rss/1024/1024 # bytes to MB
    elapsed = datetime.now() - created
    print(f'Parsed {filename} via inmemory\n elapsed: {elapsed}\n memory before: {mem_before}\n memory after: {mem_after}\n consumed: {mem_after - mem_before}')

def genJSON(ultinum=5000, legacynum=2000, filename=r"C:\Users\ricardogu\Desktop\test4.json"):
    """ 
    Build a sample JSON file.
    """
    ultipro = []
    for i in range(ultinum):
        ultipro.append({'company_name':f'RKO{i:06} Inc.', 'ar_number':f'AR{i:06}'})

    standalone = []
    empcounts = [500, 1000, 2000]
    locations = ['Town1, TX, USA', 'Town1, FL, USA', 'Town1, NY, USA', 'Town1, CA, USA', 'Town1, AZ, USA', 'Town1, IL, USA', 'Town1, CO, USA', 'Town1, ONT, CAN', 'Town1, CAL, CAN', 'Town1, BC, CAN', 'Town1, BR, CAN', 'Town1, MON, CAN', 'Town1, DF, MEX', 'Town1, LYON, FRA', 'Quay1, SING, SGP', 
                 'Town2, TX, USA', 'Town2, FL, USA', 'Town2, NY, USA', 'Town2, CA, USA', 'Town2, AZ, USA', 'Town2, IL, USA', 'Town2, CO, USA', 'Town2, ONT, CAN', 'Town2, CAL, CAN', 'Town2, BC, CAN', 'Town2, BR, CAN', 'Town2, MON, CAN', 'Town2, DF, MEX', 'Town2, LYON, FRA', 'Quay2, SING, SGP', 
                 'Town3, TX, USA', 'Town3, FL, USA', 'Town3, NY, USA', 'Town3, CA, USA', 'Town3, AZ, USA', 'Town3, IL, USA', 'Town3, CO, USA', 'Town3, ONT, CAN', 'Town3, CAL, CAN', 'Town3, BC, CAN', 'Town3, BR, CAN', 'Town3, MON, CAN', 'Town3, DF, MEX', 'Town3, LYON, FRA', 'Quay3, SING, SGP', 
                 'Town4, TX, USA', 'Town4, FL, USA', 'Town4, NY, USA', 'Town4, CA, USA', 'Town4, AZ, USA', 'Town4, IL, USA', 'Town4, CO, USA', 'Town4, ONT, CAN', 'Town4, CAL, CAN', 'Town4, BC, CAN', 'Town4, BR, CAN', 'Town4, MON, CAN', 'Town4, DF, MEX', 'Town4, LYON, FRA', 'Quay4, SING, SGP', 
                 'Town5, TX, USA', 'Town5, FL, USA', 'Town5, NY, USA', 'Town5, CA, USA', 'Town5, AZ, USA', 'Town5, IL, USA', 'Town5, CO, USA', 'Town5, ONT, CAN', 'Town5, CAL, CAN', 'Town5, BC, CAN', 'Town5, BR, CAN', 'Town5, MON, CAN', 'Town5, DF, MEX', 'Town5, LYON, FRA', 'Quay5, SING, SGP', 
                 'Town6, TX, USA', 'Town6, FL, USA', 'Town6, NY, USA', 'Town6, CA, USA', 'Town6, AZ, USA', 'Town6, IL, USA', 'Town6, CO, USA', 'Town6, ONT, CAN', 'Town6, CAL, CAN', 'Town6, BC, CAN', 'Town6, BR, CAN', 'Town6, MON, CAN', 'Town6, DF, MEX', 'Town6, LYON, FRA', 'Quay6, SING, SGP', 
                 'Town7, TX, USA', 'Town7, FL, USA', 'Town7, NY, USA', 'Town7, CA, USA', 'Town7, AZ, USA', 'Town7, IL, USA', 'Town7, CO, USA', 'Town7, ONT, CAN', 'Town7, CAL, CAN', 'Town7, BC, CAN', 'Town7, BR, CAN', 'Town7, MON, CAN', 'Town7, DF, MEX', 'Town7, LYON, FRA', 'Quay7, SING, SGP', 
                 'Town8, TX, USA', 'Town8, FL, USA', 'Town8, NY, USA', 'Town8, CA, USA', 'Town8, AZ, USA', 'Town8, IL, USA', 'Town8, CO, USA', 'Town8, ONT, CAN', 'Town8, CAL, CAN', 'Town8, BC, CAN', 'Town8, BR, CAN', 'Town8, MON, CAN', 'Town8, DF, MEX', 'Town8, LYON, FRA', 'Quay8, SING, SGP'
            ]
    
    for i in range(ultinum, ultinum+legacynum):

        employees = []
        for j in range(choice(empcounts)):
            employees.append({'id':f'ID{j:09}', 'location':f'{choice(locations)}'})

        standalone.append({'employee_info': employees, 'company_name':f'RKO{i:06} Inc.', 'ar_number':f'AR{i:06}'})

    doc = {}
    doc['server_db'] = 'prod-atl-per-mysql-1'
    doc['server_name'] = 'prod-phx-per-app-1'
    doc['ultipro'] = ultipro
    doc['standalone'] = standalone

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(obj=doc, fp=f, indent=4)
    except Exception as e:
        print(f'Error: {e}')

def main():
    """"""
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help='Specifies the json file to import')
    parser.add_argument('--mode', help='Specifies the import mode (stream or inmemory)')
    args = parser.parse_args()

    filename = None

    if args.filename:
        filename = args.filename
    else:
        filename = r"C:\Users\ricardogu\Desktop\JSONData\test_A.json"

    #genJSON(ultinum=6000, legacynum=3200, filename=r"C:\Users\ricardogu\Desktop\JSONData\test_F.json")

    if args.mode == 'inmemory':
        parseJSON(filename)
    else:
        parseiJSON(filename)

    input('Press enter to quit...')