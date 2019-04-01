#!/usr/bin/env python3
import bluetooth
import os
import time
import json
import requests
from sense_hat import SenseHat
from utils.data_access import DataAccess
from utils.file_access import FileAccess
from utils.enums import SensorDataCol


class GreenhouseBluetooth:
    ENDPOINT = 'https://api.pushbullet.com/v2/pushes'

    def __init__(self):
        token_dict = FileAccess.json_to_dict('/home/pi/Workspaces/GreenhouseMonitor/token.json')
        self.__token = token_dict['pushbullet'] if token_dict is not None else None
        self.__dao = DataAccess()

    def send_notification(self, title, body):
        if self.__token is None:
            print('No PushBullet API Token found, notification will not be sent.')
            return

        content = {"type": "note", "title": title, "body": body}

        response = requests.post(GreenhouseBluetooth.ENDPOINT, data=json.dumps(content),
                                 headers={'Access-Token': self.__token,
                                          'Content-Type': 'application/json'})

        if response.status_code != 200:
            print('Oops...Something went wrong...')
        else:
            self.__dao.log_notification()
            print('Success! Notification sent!')

    # Search for device based on device's name.
    def search(self,reading, temp_verified_result, humid_verified_result):
        notification_sent_today = self.__dao.get_notification_status()

        if not notification_sent_today:
            device_name = "Darren"
            device_address = None
            nearby_devices = bluetooth.discover_devices()

            for mac_address in nearby_devices:
                if device_name == bluetooth.lookup_name(mac_address):
                    device_address = mac_address
                    break
            if device_address is not None:
                title = 'Attention! Reading Out Of Range!'
                temp_info = temp_verified_result[1]
                humid_info = humid_verified_result[1]
                collected_time = reading[SensorDataCol.COLLECTED_AT].\
                    strftime('%b %d, %Y %I:%M:%S %p %Z')
                body =  "Hi {name}! The Phone {address} is connected! Time: {time} Temperature: {temp} \xb0C Humidity: {humid}%\n{temp_info}" \
                   "\n{humid_info}".format(name=device_name, address=device_address, time=collected_time, temp=reading[SensorDataCol.TEMP],
                                           humid=reading[SensorDataCol.HUMID], temp_info=temp_info,
                                           humid_info=humid_info)
                self.send_notification(title, body)
             
            else:
                title = 'Could not find target device nearby...'
                body = None
                self.send_notification(title, body)
                
