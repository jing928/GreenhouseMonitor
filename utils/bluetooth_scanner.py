import subprocess as sp
import re
import bluetooth
import notifier
from data_collector import DataCollector


class BluetoothScanner:

    def __init__(self):
        self.__data_collector = DataCollector()
        self.__notifier = notifier.Notifier()

    def search_and_notify(self):
        paired_devices = BluetoothScanner.get_paired_devices()
        nearby_devices = BluetoothScanner.get_nearby_devices()
        for mac_address in nearby_devices:
            if mac_address in paired_devices:
                name = paired_devices[mac_address]
                sensor_reading = self.__data_collector.collect_data()
                self.__notifier.notify_nearby_device(name, sensor_reading)

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
