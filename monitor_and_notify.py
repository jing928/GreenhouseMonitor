from utils.data_monitor import DataMonitor


class MonitorAndNotify:

    @staticmethod
    def run():
        monitor = DataMonitor()
        monitor.start_monitor()


if __name__ == '__main__':
    MonitorAndNotify.run()
