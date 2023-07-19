from PyQt5.QtWidgets import QDialog, QStackedWidget, QTableView, QComboBox, QPushButton, QLineEdit, QHeaderView, QWidget, QGridLayout
from src.connection import DAO
from win32api import GetSystemMetrics
from src.TableModel import TableModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from src.addrecordwidget import AddRecord
import regex
import PyQt5.QtCore
import PyQt5.QtWidgets


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Application')

        self.setupWidgets()

        self.UI()

        self.tableChoice.currentIndexChanged.connect(self.itemChanged)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.searchLine.textChanged.connect(self.searchRecord)

    def setupWidgets(self):
        self.dao = DAO()
        self.columns = []
        self.windowManager = QStackedWidget()
        self.windowManager.addWidget(self)
        self.searchFilter = QSortFilterProxyModel()

        self.table = QTableView()
        self.tableChoice = QComboBox(self)
        #self.widgetLayout = QWidget(self)

        self.addButton = QPushButton('Добавить запись')
        self.editButton = QPushButton('Редактировать запись')
        self.searchChoice = QComboBox()
        self.searchLine = QLineEdit()

        self.searchSignal = PyQt5.QtCore.pyqtSignal(int, QWidget)

    def searchRecord(self):
        index = self.searchChoice.currentIndex()
        self.searchFilter.setFilterKeyColumn(index)
        self.table.setModel(self.searchFilter)
        self.searchFilter.setFilterRegExp(self.searchLine.text())

    def UI(self):
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.editButton, 1, 0)
        buttonLayout.addWidget(self.tableChoice, 3, 0)
        buttonLayout.addWidget(QPushButton('Поиск записи'), 2, 0)
        buttonLayout.addWidget(self.searchLine, 0, 1)
        buttonLayout.addWidget(self.searchChoice, 0, 2)
        buttonLayout.addWidget(self.table, 1, 1, 8, 8, Qt.AlignTop)

        self.setLayout(buttonLayout)

        self.dao.exec("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema = 'public'""")

        for tableName in self.dao.getFromSelect():
            self.tableChoice.addItem(tableName[0])

        self.searchFilter.setFilterCaseSensitivity(Qt.CaseSensitive)

        self.setTable()
        self.windowManager.show()

        self.setMinimumSize(GetSystemMetrics(0)/3, GetSystemMetrics(1)/3)

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

        self.searchChoice.clear()
        for column in self.columns:
            self.searchChoice.addItem(column)

        # path to qpixmap inside cell
        photos = []
        for row in data:
            for column in self.columns:
                if column == 'photo':
                    pixmap = QPixmap(row[self.columns.index(column)])
                    photos.append(pixmap)

        model = TableModel(data, self.columns, photos)
        self.searchFilter.setSourceModel(model)
        self.table.setModel(model)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
