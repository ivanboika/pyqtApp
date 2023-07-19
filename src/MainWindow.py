from PyQt5.QtWidgets import *
from src.connection import DAO
from win32api import GetSystemMetrics
from src.TableModel import TableModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from src.addrecordwidget import AddRecord


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Application')
        self.setGeometry(0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

        self.dao = DAO()
        self.columns = []
        self.windowManager = QStackedWidget()
        self.windowManager.addWidget(self)

        self.table = QTableView(self)
        self.tableChoice = QComboBox(self)
        self.widgetLayout = QWidget(self)

        self.addButton = QPushButton('Добавить запись')
        self.editButton = QPushButton('Редактировать запись')

        self.UI()

        self.tableChoice.currentIndexChanged.connect(self.itemChanged)
        self.addButton.clicked.connect(self.addButtonClicked)

    def UI(self):
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.editButton, 1, 0)
        buttonLayout.addWidget(self.tableChoice, 3, 0)
        buttonLayout.addWidget(QPushButton('Поиск записи'), 2, 0)
        buttonLayout.addWidget(self.table, 0, 1, 8, 8, Qt.AlignTop)
        #buttonLayout.setAlignment(Qt.AlignLeft)

        self.setLayout(buttonLayout)

        #self.widgetLayout.setLayout(buttonLayout)
        #self.widgetLayout.adjustSize()

        self.dao.exec("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema = 'public'""")

        for tableName in self.dao.getFromSelect():
            self.tableChoice.addItem(tableName[0])

        self.setTable()
        self.windowManager.show()

    def itemChanged(self):
        self.setTable()

    def addButtonClicked(self):
        window = AddRecord(self.dao, self.columns, self.tableChoice.currentText())

        self.windowManager.addWidget(window)
        self.windowManager.setCurrentWidget(window)
        if window.run():
            self.setTable()
            self.adjustSize()

        self.windowManager.setCurrentWidget(self)

    def setTable(self):
        self.dao.exec('SELECT * FROM ' +
                      self.tableChoice.currentText())

        data = self.dao.getFromSelect()
        self.columns = self.dao.getColumnNames(self.tableChoice.currentText())

        # path to qpixmap inside cell
        photos = []
        for row in data:
            for column in self.columns:
                if column == 'photo':
                    pixmap = QPixmap(row[self.columns.index(column)])
                    photos.append(pixmap)

        model = TableModel(data, self.columns, photos)
        self.table.setModel(model)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

