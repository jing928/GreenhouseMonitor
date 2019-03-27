import sqlite3 as lite
from datetime import datetime, date, timezone
from utils.enums import SensorDataCol


class DataAccess:

    def __init__(self):
        self.con = lite.connect('greenhouse_monitor.db')  # Need to be full path for cronjob
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS SENSOR_DATA "
                        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "collected_at DATETIME, temp NUMERIC, humid NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS NOTIFICATION_STATUS "
                        "(id INTEGER PRIMARY KEY AUTOINCREMENT, notify_date DATE, sent BOOLEAN)")

    def __del__(self):
        self.con.close()

    def log_data(self, temp, humid):
        now = datetime.utcnow()
        cur = self.con.cursor()
        cur.execute("INSERT INTO SENSOR_DATA (collected_at, temp, humid) "
                    "VALUES (?, ?, ?)", (now, temp, humid))
        self.con.commit()

    def log_notification(self):
        today = date.today()  # Local current date
        cur = self.con.cursor()
        cur.execute("INSERT INTO NOTIFICATION_STATUS (notify_date, sent) "
                    "VALUES (?, ?)", (today, True))
        self.con.commit()
        return cur.lastrowid  # Use this to find the row inserted later

    def get_notification_status(self, lookup_date=date.today()):
        cur = self.con.cursor()
        cur.execute("SELECT sent FROM NOTIFICATION_STATUS WHERE notify_date = ?", (lookup_date,))
        result = cur.fetchone()
        if result is None:
            return False
        return result[1]  # Should return the second column of `sent (boolean)`

    def get_sensor_reading(self, row_id):
        cur = self.con.cursor()
        cur.execute("SELECT collected_at, temp, humid FROM SENSOR_DATA WHERE id = ?",
                    (row_id,))
        result = cur.fetchone()
        if result is None:
            return {}
        collected_local_time = self.utc_to_localtime(result[0])
        return {SensorDataCol.COLLECTED_AT: collected_local_time, SensorDataCol.TEMP: result[1],
                SensorDataCol.HUMID: result[2]}

    @staticmethod
    def utc_to_localtime(utc_time):
        return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
