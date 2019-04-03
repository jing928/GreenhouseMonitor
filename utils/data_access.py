import sqlite3 as lite
import pandas as pd
from datetime import datetime, date, timezone
from utils.enums import SensorDataCol


class DataAccess:

    def __init__(self):
        self.con = lite.connect('/home/pi/Workspaces/GreenhouseMonitor/greenhouse_monitor.db',
                                detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS SENSOR_DATA "
                        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "collected_at TIMESTAMP, temp NUMERIC, humid NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS NOTIFICATION_STATUS "
                        "(id INTEGER PRIMARY KEY AUTOINCREMENT, notify_date DATE, sent BOOLEAN)")
            cur.execute("CREATE TABLE IF NOT EXISTS BT_NOTIFICATION_TIME "
                        "(id INTEGER PRIMARY KEY AUTOINCREMENT, sent_time TIMESTAMP)")

    def __del__(self):
        self.con.close()

    def log_data(self, temp, humid):
        now = datetime.utcnow()
        cur = self.con.cursor()
        cur.execute("INSERT INTO SENSOR_DATA (collected_at, temp, humid) "
                    "VALUES (?, ?, ?)", (now, temp, humid))
        self.con.commit()
        return cur.lastrowid  # Use this to find the row inserted later

    def log_notification(self):
        today = date.today()  # Local current date
        cur = self.con.cursor()
        cur.execute("INSERT INTO NOTIFICATION_STATUS (notify_date, sent) "
                    "VALUES (?, ?)", (today, True))
        self.con.commit()

    def log_bt_notification_time(self):
        now = datetime.utcnow()
        cur = self.con.cursor()
        cur.execute("INSERT INTO BT_NOTIFICATION_TIME (sent_time) VALUES (?)", (now, ))
        self.con.commit()

    def get_last_bt_notification_time(self):
        cur = self.con.cursor()
        cur.execute("SELECT sent_time FROM BT_NOTIFICATION_TIME ORDER BY id DESC LIMIT 1")
        result = cur.fetchone()
        if result is None:
            return datetime(year=1900, month=1, day=1)  # A default time in the past
        return result[0]

    def get_notification_status(self, lookup_date=date.today()):
        cur = self.con.cursor()
        cur.execute("SELECT sent FROM NOTIFICATION_STATUS WHERE notify_date = ?", (lookup_date, ))
        result = cur.fetchone()
        if result is None:
            return False
        return result[0]  # Should return the second column of `sent (boolean)`

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

    def get_distinct_local_days(self):
        cur = self.con.cursor()
        cur.execute("SELECT DISTINCT DATE(collected_at, 'localtime', 'start of day') "
                    "FROM SENSOR_DATA")
        results = cur.fetchall()
        return results

    def get_max_temp_of_day(self, day):
        cur = self.con.cursor()
        cur.execute("SELECT MAX(temp) FROM SENSOR_DATA "
                    "WHERE DATE(collected_at, 'localtime', 'start of day') = ?", (day, ))
        result = cur.fetchone()
        return result[0]

    def get_min_temp_of_day(self, day):
        cur = self.con.cursor()
        cur.execute("SELECT MIN(temp) FROM SENSOR_DATA "
                    "WHERE DATE(collected_at, 'localtime', 'start of day') = ?", (day,))
        result = cur.fetchone()
        return result[0]

    def get_max_humid_of_day(self, day):
        cur = self.con.cursor()
        cur.execute("SELECT MAX(humid) FROM SENSOR_DATA "
                    "WHERE DATE(collected_at, 'localtime', 'start of day') = ?", (day,))
        result = cur.fetchone()
        return result[0]

    def get_min_humid_of_day(self, day):
        cur = self.con.cursor()
        cur.execute("SELECT MIN(humid) FROM SENSOR_DATA "
                    "WHERE DATE(collected_at, 'localtime', 'start of day') = ?", (day,))
        result = cur.fetchone()
        return result[0]

    def get_all_sensor_data(self):
        return pd.read_sql_query("SELECT DATETIME(collected_at, 'localtime') as 'time', "
                                 "temp, humid FROM SENSOR_DATA", self.con)

    @staticmethod
    def utc_to_localtime(utc_time):
        return utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
