import sqlite3 as lite
from datetime import datetime, date


class DataAccess:

    def __init__(self):
        self.con = lite.connect('greenhouse_monitor.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS SENSOR_DATA"
                        "(timestamp DATETIME, temp NUMERIC, humid NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS NOTIFICATION_STATUS (date DATE, sent BOOLEAN)")

    def __del__(self):
        self.con.close()

    def log_data(self, temp, humid):
        now = datetime.utcnow()
        cur = self.con.cursor()
        cur.execute("INSERT INTO SENSOR_DATA VALUES (?, ?, ?)", (now,), (temp,), (humid,))
        self.con.commit()

    def log_notification(self):
        today = date.today()  # Local current date
        cur = self.con.cursor()
        cur.execute("INSERT INTO NOTIFICATION_STATUS VALUES (?, ?)", (today,), (True,))
        self.con.commit()

    def get_notification_status(self, current_date):
        cur = self.con.cursor()
        cur.execute("SELECT sent FROM NOTIFICATION_STATUS WHERE date = ?", (current_date,))
        result = cur.fetchone()
        if result is None:
            return False
        return result[1]  # Should return the second column of `sent (boolean)`
