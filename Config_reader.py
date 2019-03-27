import json
import os.path


class ConfigReader:
        @staticmethod
        def read_file(path):
            p, file = os.path.split(path)
            print("f is " + file)
            try:
                readfile = open(file, "r")
            except ValueError:
                print("The path is not existed!")
            loadfile = json.load(readfile)
            return loadfile


ConfigReader.read_file("../GreenhouseMonitor/Config_reader.py")
