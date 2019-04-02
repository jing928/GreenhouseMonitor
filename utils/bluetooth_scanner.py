import subprocess as sp
import re
from datetime import datetime
import bluetooth
from utils.notifier import Notifier
from utils.data_collector import DataCollector
from utils.data_access import DataAccess


class BluetoothScanner:

    def __init__(self):
        self.__dao = DataAccess()
        self.__data_collector = DataCollector()
        self.__notifier = Notifier()

    def search_and_notify(self):
        paired_devices = BluetoothScanner.get_paired_devices()
        nearby_devices = BluetoothScanner.get_nearby_devices()
        for mac_address in nearby_devices:
            if mac_address in paired_devices:
                name = paired_devices[mac_address]
                self.__notify(name)
                break

    def __notify(self, name):
        if self.__verify_frequency():
            sensor_reading = self.__data_collector.collect_data()
            self.__notifier.notify_nearby_device(name, sensor_reading)

    def __verify_frequency(self):
        last_sent_time = self.__dao.get_last_bt_notification_time()
        now = datetime.utcnow()
        diff = now - last_sent_time
        time_elapsed = diff.total_seconds()
        if time_elapsed > 60:  # Notification frequency should be greater than a minute
            return True
        print('Maximum frequency reached!')
        return False

    # Modified from the script provided by PIoT course
    @staticmethod
    def get_paired_devices():
        process_output = sp.Popen(["bt-device", "--list"],
                                  stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
        stdout = process_output.stdout
        raw_data = stdout.readlines()[1:]  # Skip header row
        devices = {}

        for line in raw_data:
            decoded_line = line.decode().strip()
            processed_line = re.sub('[()]', '', decoded_line)  # Remove parentheses
            device_info = processed_line.split(' ')
            device_name = device_info[0]
            device_address = device_info[1]
            devices[device_address] = device_name

        return devices

    @staticmethod
    def get_nearby_devices():
        return bluetooth.discover_devices()
