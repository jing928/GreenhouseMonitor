import sqlite3 as lite


class DataAccess:

    def __init__(self):
        self.con = lite.connect('greenhouse_monitor.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS "
                        "SENSOR_DATA(timestamp DATETIME, temp NUMERIC, humid NUMERIC)")
            cur.execute("CREATE TABLE IF NOT EXISTS "
                        "NOTIFICATION_STATUS(date DATE, sent BOOLEAN)")
