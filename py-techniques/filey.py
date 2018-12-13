from datetime import date
import os.path

def pickFiles(src):
    newfiles = []
    
    try:

        processdate = date.today()
        with os.scandir(path=src) as d:
            for entry in d: # os.DirEntry
                ctime = entry.stat().st_ctime
                filedate = date.fromtimestamp(ctime)
                #filedate = date.fromtimestamp(os.path.getctime(entry.path))

                if entry.is_file() and processdate == filedate:
                    newfiles.append(entry.path)

            for fi in newfiles:
                print(fi)

    except Exception as e: # catch all
        print(f'pickFiles: {e}')

pickFiles(r'C:\Users\rguzman\Desktop\Personal\Logistics')
