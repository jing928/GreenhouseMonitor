from utils.figure_generator import FigureGenerator


class Analytics:

    @staticmethod
    def run():
        generator = FigureGenerator()
        generator.generate_line_chart()
        generator.generate_joint_plot()


if __name__ == '__main__':
    Analytics.run()
