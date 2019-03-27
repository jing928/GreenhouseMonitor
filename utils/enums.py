from enum import Enum


class SensorType(Enum):

    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'


class SensorDataCol(Enum):

    COLLECTED_AT = 'collected_at'
    TEMP = 'temp'
    HUMID = 'humid'
