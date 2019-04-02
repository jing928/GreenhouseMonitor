class Validator:

    @staticmethod
    def verify_temp(temp, data_range):
        min_temp = data_range['min_temperature']
        max_temp = data_range['max_temperature']
        if temp > max_temp:
            diff = temp - max_temp
            result = Validator.above_max_temp_result(diff)
        elif temp < min_temp:
            diff = min_temp - temp
            result = Validator.below_min_temp_result(diff)
        else:
            result = Validator.within_range_result()

        return result

    @staticmethod
    def verify_humid(humid, data_range):
        min_humid = data_range['min_humidity']
        max_humid = data_range['max_humidity']
        if humid > max_humid:
            diff = humid - max_humid
            result = Validator.above_max_humid_result(diff)
        elif humid < min_humid:
            diff = min_humid - humid
            result = Validator.below_min_humid_result(diff)
        else:
            result = Validator.within_range_result()

        return result

    @staticmethod
    def verify_temp_humid_of_day(min_temp, max_temp, min_humid, max_humid, data_range):
        temp_result = Validator.verify_min_max_temp_of_day(min_temp, max_temp, data_range)
        humid_result = Validator.verify_min_max_humid_of_day(min_humid, max_humid, data_range)
        return Validator.aggregate_two_results(temp_result, humid_result)

    @staticmethod
    def verify_min_max_temp_of_day(min_temp_day, max_temp_day, data_range):
        min_temp = data_range['min_temperature']
        max_temp = data_range['max_temperature']
        if min_temp_day < min_temp:
            min_result = Validator.below_min_temp_result(min_temp - min_temp_day)
        else:
            min_result = Validator.within_range_result()
        if max_temp_day > max_temp:
            max_result = Validator.above_max_temp_result(max_temp_day - max_temp)
        else:
            max_result = Validator.within_range_result()
        return Validator.aggregate_two_results(max_result, min_result)

    @staticmethod
    def verify_min_max_humid_of_day(min_humid_day, max_humid_day, data_range):
        min_humid = data_range['min_humidity']
        max_humid = data_range['max_humidity']
        if min_humid_day < min_humid:
            min_result = Validator.below_min_humid_result(min_humid - min_humid_day)
        else:
            min_result = Validator.within_range_result()
        if max_humid_day > max_humid:
            max_result = Validator.above_max_humid_result(max_humid_day - max_humid)
        else:
            max_result = Validator.within_range_result()
        return Validator.aggregate_two_results(max_result, min_result)

    @staticmethod
    def aggregate_two_results(result_1, result_2):
        if not result_1[0] and not result_2[0]:
            return False, result_1[1] + ' ' + result_2[1]
        if not result_1[0]:
            return False, result_1[1]
        if not result_2[0]:
            return False, result_2[1]
        return Validator.within_range_result()

    @staticmethod
    def within_range_result():
        return True, 'OK'

    @staticmethod
    def above_max_temp_result(diff):
        return False, "{0:.1f} *C above maximum temperature".format(diff)

    @staticmethod
    def below_min_temp_result(diff):
        return False, "{0:.1f} *C below minimum temperature".format(diff)

    @staticmethod
    def above_max_humid_result(diff):
        return False, "{0:.1f}% above maximum humidity".format(diff)

    @staticmethod
    def below_min_humid_result(diff):
        return False, "{0:.1f}% below minimum humidity".format(diff)
