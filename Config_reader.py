import json
# from pathlib import Path


class ConfigReader:

        @staticmethod
        def read_file(path):
            try:
                readfile = open(path, "r")
            except ValueError:
                print("The path is not existed!")
            finally:
                loadfile = json.load(readfile)
                return loadfile




# ConfigReader.read_file()