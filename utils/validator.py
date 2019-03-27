class Validator:

    @staticmethod
    def verify_temp(temp, data_range):
        min_temp = data_range['min_temperature']
        max_temp = data_range['max_temperature']
        if temp > max_temp:
            diff = temp - max_temp
            result = (False, "{0:.1f} *C above maximum temperature".format(diff))
        elif temp < min_temp:
            diff = min_temp - temp
            result = (False, "{0:.1f} *C below minimum temperature".format(diff))
        else:
            result = (True, "OK")

        return result

    @staticmethod
    def verify_humid(humid, data_range):
        min_humid = data_range['min_humidity']
        max_humid = data_range['max_humidity']
        if humid > max_humid:
            diff = humid - max_humid
            result = (False, "{0:.1f}% above maximum humidity".format(diff))
        elif humid < min_humid:
            diff = min_humid - humid
            result = (False, "{0:.1f}% below minimum humidity".format(diff))
        else:
            result = (True, "OK")

        return result
