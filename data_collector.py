from sense_hat import SenseHat
from data_access import DataAccess


class DataCollector:

    def __init__(self):
        self.sense = SenseHat()

    def collect_data(self):
        temp = self.collect_temp()
        humid = self.collect_humid()
        if temp is not None and humid is not None:
            dao = DataAccess()
            dao.log_data(temp, humid)

    def collect_temp(self):
        temp = self.sense.get_temperature()
        return None if temp == 0 else temp

    def collect_humid(self):
        humid = self.sense.get_humidity()
        return None if humid == 0 else humid
