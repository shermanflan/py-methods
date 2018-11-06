import json

def main():
    try:

        with open("C:\\Users\\ricardogu\\Desktop\\test.json", "r", encoding="utf-8") as f:
            
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

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
