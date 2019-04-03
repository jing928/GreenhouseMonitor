import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas.plotting import register_matplotlib_converters
from utils.data_access import DataAccess


class FigureGenerator:

    def __init__(self):
        dao = DataAccess()
        self.__sensor_data = dao.get_all_sensor_data()

    def generate_line_chart(self):
        print('Generating line chart...')
        register_matplotlib_converters()
        axes = plt.gca()
        axes.xaxis.set_major_locator(mpl.dates.DayLocator())
        axes.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m/%Y'))
        axes.xaxis.set_minor_locator(mpl.dates.HourLocator(interval=8))
        axes.xaxis.set_minor_formatter(mpl.dates.DateFormatter('%H:%M'))
        axes.xaxis.set_tick_params(which='major', pad=10, labelsize=8)
        axes.xaxis.set_tick_params(which='minor', labelsize=5)

        plt.title('Line Chart: Temperature vs Humidity')
        plt.ylabel('\xb0C | %')
        plt.xlabel('Reading Collected Time')
        plt.plot('time', 'temp', data=self.__sensor_data,
                 marker='', color='tomato', label='Temperature')
        plt.plot('time', 'humid', data=self.__sensor_data,
                 marker='', color='turquoise', label='Humidity')
        plt.legend()
        plt.savefig('line_chart.png', dpi=400, bbox_inches='tight')
        print('Finished.')
