from utils.report_generator import ReportGenerator


class CreateReport:

    @staticmethod
    def run():
        generator = ReportGenerator()
        generator.get_user_input()
        generator.generate()


if __name__ == '__main__':
    CreateReport.run()
