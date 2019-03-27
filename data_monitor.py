from utils.data_access import DataAccess
from utils.file_access import FileAccess
from utils.enums import SensorType, SensorDataCol
from utils.validator import Validator
from data_collector import DataCollector
from notifier import Notifier


class DataMonitor:

    def __init__(self):
        self.__data_collector = DataCollector()
        self.__dao = DataAccess()
        self.__notifier = Notifier()

    def start_monitor(self):
        sensor_data = self.__data_collector.collect_data()
        if sensor_data is not None:
            row_id = self.__save_data(sensor_data)
            self.__verify_range(row_id)

    def __save_data(self, data):
        return self.__dao.log_data(data[SensorType.TEMPERATURE], data[SensorType.HUMIDITY])

    def __verify_range(self, row_id):
        reading = self.__dao.get_sensor_reading(row_id)
        if not reading:
            print('No reading saved.')
            return
        
        sensor_data_range = FileAccess.json_to_dict('/home/pi/Workspaces/GreenhouseMonitor/'
                                                    'config.json')
        if sensor_data_range is None:
            print('No range config available. Cannot verify...')
            return

        result_temp = Validator.verify_temp(reading[SensorDataCol.TEMP], sensor_data_range)
        result_humid = Validator.verify_humid(reading[SensorDataCol.TEMP], sensor_data_range)
        temp_within_range = result_temp[0]
        humid_within_range = result_humid[0]
        if not (temp_within_range and humid_within_range):
            self.__notifier.notify_out_of_range_reading(reading, result_temp, result_humid)
