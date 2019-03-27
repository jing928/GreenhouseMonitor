import json
from pathlib import Path


class ConfigReader:

    try:
        @staticmethod
        def read_file(path):     # the parameter is a path
            #path = Path('GreenhouseMonitor', 'config.json')
            readfile = open(path, "r")    # do not write path, that should be a parameter
            loadfile = json.load(readfile)
            return loadfile
            # print(f.read())
    except ValueError:
        print("The path is not existed!")


#ConfigReader.read_file()