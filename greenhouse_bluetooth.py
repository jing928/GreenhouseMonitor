import time
from utils.bluetooth_scanner import BluetoothScanner


class GreenhouseBluetooth:

    @staticmethod
    def run():
        scanner = BluetoothScanner()
        while True:
            scanner.search_and_notify()
            time.sleep(5)


if __name__ == '__main__':
    GreenhouseBluetooth.run()
