from sense_hat import SenseHat


class DataCollector:

    def __init__(self):
        self.__sense = SenseHat()

    def collect_data(self):
        temp = self.collect_temp()
        humid = self.collect_humid()
        if temp is not None and humid is not None:
            return {'temperature': round(temp, 1), 'humidity': round(humid, 1)}
        else:
            return None

    def collect_temp(self):
        temp = self.__sense.get_temperature()
        return None if temp == 0 else temp

    def collect_humid(self):
        humid = self.__sense.get_humidity()
        return None if humid == 0 else humid
