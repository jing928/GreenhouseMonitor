import os
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
        temp = self.get_calibrated_temperature()
        return None if temp == 0 else temp

    def collect_humid(self):
        humid = self.__sense.get_humidity()
        return None if humid == 0 else humid

    # Begin Reference
    # The temperature correction code below is modified from
    # http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    @staticmethod
    def get_cpu_temperature():
        response = os.popen("vcgencmd measure_temp").readline()
        temp = float(response.replace('temp=', '').replace("'C\n", ''))
        return temp

    def get_calibrated_temperature(self):
        temp_from_humid = self.__sense.get_temperature_from_humidity()
        if temp_from_humid == 0:
            return 0
        temp_from_pressure = self.__sense.get_temperature_from_pressure()
        if temp_from_pressure == 0:
            return 0
        temp_cpu = self.get_cpu_temperature()

        temp_average_humid_pressure = (temp_from_humid + temp_from_pressure) / 2
        temp_corrected = temp_average_humid_pressure - ((temp_cpu - temp_average_humid_pressure) / 1.5)
        return temp_corrected
    # End of Reference
