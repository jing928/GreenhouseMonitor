import json
import csv


class FileAccess:

    @staticmethod
    def json_to_dict(path):
        try:
            readfile = open(path, 'r')
        except OSError:
            print('Oops...Cannot open the file...')
            return None
        else:
            with readfile:
                content_dict = json.load(readfile)
                return content_dict

    @staticmethod
    def write_to_csv(data, path):
        # data is a list of lists representing each row
        try:
            csv_file = open(path, 'w')
        except OSError:
            print('Oops...Invalid path...Please try again.')
        else:
            with csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data)
            csv_file.close()
