from utils.report_generator import ReportGenerator


class CreateReport:

    @staticmethod
    def run():
        generator = ReportGenerator()
        generator.generate()


if __name__ == '__main__':
    CreateReport.run()
