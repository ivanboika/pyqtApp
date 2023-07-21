from src.View.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

class Start:
    def __init__(self):
        app = QApplication([])
        window = MainWindow()
        window.show()
        app.exec_()
