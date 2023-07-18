from src.MainWindow import *


class Start:
    def __init__(self):
        app = QApplication([])
        window = MainWindow()
        window.show()
        app.exec_()
