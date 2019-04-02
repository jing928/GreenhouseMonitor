import json
import requests
import bluetooth
import sqlite3
from utils.data_access import DataAccess
from utils.file_access import FileAccess
from utils.enums import SensorDataCol
import notifier

class GreenhouseBluetooth:
    

   

    # Search for device based on device's name.
    def search(self):
        nearby_devices = bluetooth.discover_devices(lookup_name = True)
        for name, mac_address in nearby_devices:
            device_name = name   
            device_address = mac_address
            connection = sqlite3.connect(bDatabase)
            cur = connection.cursor()
            cur.fetchone()
            cur.execute("SELECT * FROM Bluetooth_Data WHERE devicename= ? AND deviceaddress= ?", (device_name, device_address))
            result = cur.fetchone()
            if result:
                title = 'Attention! Reading Out Of Range!'
               
               
                notifier.send_notification(title, body)
            else:
                title = 'Could not find target device nearby...'
                body = None
                self.send_notification(title, body)
