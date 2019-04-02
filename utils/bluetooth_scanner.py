import subprocess as sp
import re
import bluetooth


class BluetoothScanner:

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
