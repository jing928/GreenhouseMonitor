import json
import requests
from utils.data_access import DataAccess
from utils.file_access import FileAccess
from utils.enums import SensorDataCol, SensorType


class Notifier:

    ENDPOINT = 'https://api.pushbullet.com/v2/pushes'

    def __init__(self):
        token_dict = FileAccess.json_to_dict('/home/pi/Workspaces/GreenhouseMonitor/token.json')
        self.__token = token_dict['pushbullet'] if token_dict is not None else None
        self.__dao = DataAccess()

    def send_notification(self, title, body):
        if self.__token is None:
            print('No PushBullet API Token found, notification will not be sent.')
            return False

        content = {"type": "note", "title": title, "body": body}

        response = requests.post(Notifier.ENDPOINT, data=json.dumps(content),
                                 headers={'Access-Token': self.__token,
                                          'Content-Type': 'application/json'})

        if response.status_code != 200:
            print('Oops...Something went wrong...')
            return False
        print('Success! Notification sent!')
        return True

    def notify_out_of_range_reading(self, reading, temp_verified_result, humid_verified_result):
        notification_sent_today = self.__dao.get_notification_status()
        if not notification_sent_today:
            title = 'Attention! Reading Out Of Range!'
            temp_info = temp_verified_result[1]
            humid_info = humid_verified_result[1]
            collected_time = reading[SensorDataCol.COLLECTED_AT].\
                strftime('%b %d, %Y %I:%M:%S %p %Z')
            body = "Time: {time} Temperature: {temp} \xb0C Humidity: {humid}%\n{temp_info}" \
                   "\n{humid_info}".format(time=collected_time, temp=reading[SensorDataCol.TEMP],
                                           humid=reading[SensorDataCol.HUMID], temp_info=temp_info,
                                           humid_info=humid_info)
            if self.send_notification(title, body):
                self.__dao.log_notification()

    def notify_nearby_device(self, device_name, reading):
        title = "Hello {name}!".format(name=device_name)
        body = "The current temperature is {temp:.1f} \xb0C and the humidity is {humid:.1f}%.\n" \
               "Have a nice day!".format(temp=reading[SensorType.TEMPERATURE],
                                         humid=reading[SensorType.HUMIDITY])
        if self.send_notification(title, body):
            self.__dao.log_bt_notification_time()
