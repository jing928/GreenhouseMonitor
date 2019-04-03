import sqlite3 as lite
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class FigureGenerator:
    @staticmethod
    def generate():
        conn = lite.connect('/home/pi/Workspaces/GreenhouseMonitor/greenhouse_monitor.db',
                            detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)

        sql_cmd = "SELECT collected_at,temp FROM SENSOR_DATA"
        df = pd.read_sql(sql=sql_cmd, con=conn)
        fig, ax = plt.subplot(figsize=(8, 5), dpi=80)
        ax.scatter(df["collected_at"], df["temp"], s=75, c="red", alpha=0.5)   # x is time, y is temperature
        # ax.scatter(df["collected_at"], df["humid"])  # x is time, y is humid

        ax.set_xlabel("collected_at", fontsize=13)
        ax.set_ylabel("temp", fontsize=13)
        ax.set_title("time and temp change")
        ax.legend()
        ax.show()


FigureGenerator.generate()
