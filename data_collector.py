from sense_hat import SenseHat
from utils.enums import SensorType


class DataCollector:

    def __init__(self):
        self.__sense = SenseHat()

    def collect_data(self):
        temp = self.collect_temp()
        humid = self.collect_humid()
        if temp is None or humid is None:
            return None
        return {SensorType.TEMPERATURE: round(temp, 1), SensorType.HUMIDITY: round(humid, 1)}

    def collect_temp(self):
        temp = self.__sense.get_temperature()
        return None if temp == 0 else temp

    def collect_humid(self):
        humid = self.__sense.get_humidity()
        return None if humid == 0 else humid
