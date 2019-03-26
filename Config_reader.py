import json


class ConfigReader:
    @staticmethod
    def read_file():     # the parameter is a path
        f = open("../GreenhouseMonitor/config.json", "r")    # do not write path, that should be a parameter
        y = json.load(f)
        print y
        # print(f.read())


ConfigReader.read_file()
