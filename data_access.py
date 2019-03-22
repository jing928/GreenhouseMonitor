import sqlite3 as lite
from datetime import datetime, date


class DataAccess:

    SENSOR_DATA_TB = 'SENSOR_DATA'
    NOTIFICATION_STATUS_TB = 'NOTIFICATION_STATUS'

    def __init__(self):
        self.con = lite.connect('greenhouse_monitor.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS "
                        "? (timestamp DATETIME, temp NUMERIC, humid NUMERIC)",
                        (DataAccess.SENSOR_DATA_TB,))
            cur.execute("CREATE TABLE IF NOT EXISTS "
                        "? (date DATE, sent BOOLEAN)",
                        (DataAccess.NOTIFICATION_STATUS_TB,))

    def __del__(self):
        self.con.close()

    def log_data(self, temp, humid):
        now = datetime.utcnow()
        cur = self.con.cursor()
        cur.execute("INSERT INTO ? VALUES (?, ?, ?)",
                    (DataAccess.SENSOR_DATA_TB,), (now,), (temp,), (humid,))
        self.con.commit()

    def log_notification(self):
        today = date.today()
        cur = self.con.cursor()
        cur.execute("INSERT INTO ? VALUES (?, ?)",
                    (DataAccess.NOTIFICATION_STATUS_TB,), (today,), (True,))
