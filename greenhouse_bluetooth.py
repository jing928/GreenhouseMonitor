from utils.bluetooth_scanner import BluetoothScanner


class GreenhouseBluetooth:

    @staticmethod
    def run():
        scanner = BluetoothScanner()
        scanner.search_and_notify()


if __name__ == '__main__':
    GreenhouseBluetooth.run()
