from data_access import DataAccess
from data_collector import DataCollector
from utils.sensor_type import SensorType


class DataMonitor:

    def __init__(self):
        self.__data_collector = DataCollector()
        self.__dao = DataAccess()

    def start_monitor(self):
        sensor_data = self.__data_collector.collect_data()
        if sensor_data is not None:
            self.__save_data(sensor_data)

    def __save_data(self, data):
        self.__dao.log_data(data[SensorType.TEMPERATURE], data[SensorType.HUMIDITY])
