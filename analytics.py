from utils.figure_generator import FigureGenerator


class Analytics:

    @staticmethod
    def run():
        generator = FigureGenerator()
        generator.generate_line_chart()


if __name__ == '__main__':
    Analytics.run()
