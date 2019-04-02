from utils.data_access import DataAccess
from utils.file_access import FileAccess
from utils.validator import Validator


class ReportGenerator:

    def __init__(self):
        self.__dao = DataAccess()
        self.__report_name = 'reports/output.csv'
        self.__report_data = [['Date', 'Status']]

    def generate(self):
        days = self.__dao.get_distinct_local_days()
        if not days:
            print('Error: No data in the database.')
            return
        sensor_data_range = FileAccess.get_sensor_data_range()
        if sensor_data_range is None:
            print('Error: No range config available.')
            return
        for day in days:
            self.__process_day(day[0], sensor_data_range)
            FileAccess.write_to_csv(self.__report_data, self.__report_name)

    def get_user_input(self):
        text = input("Please enter the report name:")
        self.__report_name = 'reports/' + text + '.csv'

    def __process_day(self, day, data_range):
        min_temp = self.__dao.get_min_temp_of_day(day)
        max_temp = self.__dao.get_max_temp_of_day(day)
        min_humid = self.__dao.get_min_humid_of_day(day)
        max_humid = self.__dao.get_max_humid_of_day(day)
        day_result = Validator.verify_temp_humid_of_day(min_temp, max_temp,
                                                        min_humid, max_humid, data_range)
        if not day_result[0]:
            day_status = 'BAD: ' + day_result[1]
        else:
            day_status = day_result[1]
        day_row = [day, day_status]
        self.__report_data.append(day_row)
