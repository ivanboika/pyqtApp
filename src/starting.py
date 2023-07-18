from src.MainWindow import *

class Start:
    def __init__(self):
        app = QApplication([])
        #app.setStyleSheet(
        #    "MainWindow {background-image: url(E:/kitten.jpg); background-repeat: no-repeat; background-position: center; background-size: cover;}")
        window = MainWindow()
        window.show()
        app.exec_()