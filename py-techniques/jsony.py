import json
import ijson
from collections import defaultdict

def parseJSON(filename="C:\\Users\\ricardogu\\Desktop\\test.json"):

    """ Using standard json library. Loads file into memory.
    """
    try:

        with open(filename, "r", encoding="utf-8") as f:
            
            jsonObj = json.load(f) # throws JSONDecodeError

            server = jsonObj['server_db']
            servername = jsonObj['server_name']
            ultipro = jsonObj['ultipro']
            standalone = jsonObj['standalone']

            print(jsonObj)
            print(server)
            print(servername)
            print(ultipro)
            print(standalone)

    except Exception as e:
        print(e)

# 
def parseiJSON(filename="C:\\Users\\ricardogu\\Desktop\\test.json"):

    """ Using ijson library allows streaming the json file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            
            # Use this to get prefix for the json elements.
            parsed = ijson.parse(f) # returns iterator
            #print('\n'.join(list(parsed)))

            server_name = server_db = None
            ultipro, standalone = [], []
            tmpCo = tmpAR = tmpEmpInfo = None

            for pre, evt, val in parsed: # returns all (prefix, event, value)
                if (pre, evt) == ('server_db', 'string'):
                    server_db = val
                elif (pre, evt) == ('server_name', 'string'):
                    server_name = val
                elif (pre, evt) == ('ultipro.item.ar_number', 'string'):
                    ultipro.append(val)
                # New standalone co
                elif (pre, evt) == ('standalone.item', 'start_map'):
                    tmpEmpInfo = defaultdict(int)
                elif (pre, evt) == ('standalone.item.employee_info.item.location', 'string'):
                    tmpEmpInfo[val] += 1
                elif (pre, evt) == ('standalone.item.company_name', 'string'):
                    tmpCo = val
                elif (pre, evt) == ('standalone.item.ar_number', 'string'):
                    tmpAR = val
                # End standalone co
                elif (pre, evt) == ('standalone.item', 'end_map'):
                    if tmpEmpInfo: # ignore N/A
                        standalone.append([tmpCo, tmpAR, tmpEmpInfo])

            print(server_db)
            print(server_name)
            print(ultipro)
            print(standalone)

            # Get server
            #serverdb = ijson.items(f, 'server_db') # returns iterator
            #servername = ijson.items(f, 'server_name') # returns iterator

            #print(list(serverdb)[0])
            #print(list(servername)[0])

            # Get standalone customers:
            #alone = ijson.items(f, 'standalone.item') # returns iterator
            
            #for co in alone:
            #    print(co['company_name']) # 
            #    print(co['ar_number']) # 
            #    print(co['employee_info']) # 
            
            # Get ultipro customers (only ar):
            #arNumber = ijson.items(f, 'ultipro.item.ar_number') # returns iterator
            
            #for ar in arNumber:
            #    print(ar)

            ## Get ultipro customers.
            #ultipro = ijson.items(f, 'ultipro.item') # returns iterator
            
            #for co in ultipro:
            #    print(co['ar_number']) # ar no


    except Exception as e:
        print(e)

def main():
    #parseJSON()
    parseiJSON()

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
