import json
import requests
from utils.data_access import DataAccess
from utils.enums import SensorDataCol


class Notifier:

    ENDPOINT = 'https://api.pushbullet.com/v2/pushes'

    def __init__(self):
        self.__token = 'o.sp3pA6LfFHgeFZlVKSjrNviwnevqAVXX'

    def send_notification(self, title, body):
        content = {"type": "note", "title": title, "body": body}

        response = requests.post(Notifier.ENDPOINT, data=json.dumps(content),
                                 headers={'Access-Token': self.__token,
                                          'Content-Type': 'application/json'})

        if response.status_code != 200:
            print('Oops...Something went wrong...')
        else:
            print('Success! Notification sent!')

    def notify_out_of_range_reading(self, reading, temp_verified_result, humid_verified_result):
        dao = DataAccess()
        notification_sent_today = dao.get_notification_status()
        if not notification_sent_today:
            title = 'Attention! Reading Out Of Range!'
            temp_info = temp_verified_result[1]
            humid_info = humid_verified_result[1]
            collected_time = reading[SensorDataCol.COLLECTED_AT]
            body = "Time: {time} Temperature: {temp} *C Humidity: {humid}%\n{temp_info}" \
                   "\n{humid_info}".format(time=collected_time, temp=reading[SensorDataCol.TEMP],
                                           humid=reading[SensorDataCol.HUMID], temp_info=temp_info,
                                           humid_info=humid_info)
            self.send_notification(title, body)
