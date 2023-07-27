from PyQt5.QtWidgets import \
    QDialog, QStackedWidget, QTableView, QComboBox, \
    QPushButton, QLineEdit, QHeaderView, QGridLayout, QAbstractItemView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSortFilterProxyModel

from src.DBAccess.Controller import Controller
from src.Model.ModelHandler import modelHandler
from src.Model.TableModel import TableModel
from src.View.AddRecordWidget import AddRecord
from src.View.EditingWindow import EditingWindow

from win32api import GetSystemMetrics
import regex as rgx


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Application')

        self.controller = Controller()

        self.setupWidgets()

        self.UI()

        self.tableChoice.currentIndexChanged.connect(self.itemChanged)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.searchLine.textChanged.connect(self.searchRecord)
        self.editButton.clicked.connect(self.editRecord)

    def setupWidgets(self):
        self.columns = []
        self.windowManager = QStackedWidget()
        self.windowManager.addWidget(self)
        self.searchFilter = QSortFilterProxyModel()

        self.table = QTableView()
        self.tableChoice = QComboBox(self)

        self.addButton = QPushButton('Добавить запись')
        self.editButton = QPushButton('Редактировать запись')
        self.searchChoice = QComboBox()
        self.searchLine = QLineEdit()

    def searchRecord(self):
        index = self.searchChoice.currentIndex()
        self.searchFilter.setFilterKeyColumn(index)
        self.table.setModel(self.searchFilter)
        self.searchFilter.setFilterRegExp(self.searchLine.text())

    def UI(self):
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.editButton, 1, 0)
        buttonLayout.addWidget(self.tableChoice, 2, 0)
        buttonLayout.addWidget(self.searchLine, 0, 1)
        buttonLayout.addWidget(self.searchChoice, 0, 2)
        buttonLayout.addWidget(self.table, 1, 1, 8, 8, Qt.AlignTop)

        self.setLayout(buttonLayout)

        tableNames = self.controller.getAllTableNames()

        for tableName in tableNames:
            self.tableChoice.addItem(tableName)

        self.searchFilter.setFilterCaseSensitivity(Qt.CaseSensitive)

        self.setTable()
        self.windowManager.show()

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setMinimumSize(GetSystemMetrics(0)/3, GetSystemMetrics(1)/3)

    def itemChanged(self):
        self.setTable()

    def addButtonClicked(self):
        window = AddRecord(self.controller, self.columns, self.tableChoice.currentText())

        self.windowManager.addWidget(window)
        self.windowManager.setCurrentWidget(window)
        if window.run():
            self.setTable()
            self.adjustSize()

        self.windowManager.setCurrentWidget(self)

    def setTable(self):
        tableData = self.controller.getDataFromTable(
            modelHandler(self.tableChoice.currentText()))

        self.columns = self.controller.getColumnNames(modelHandler(self.tableChoice.currentText()))

        self.searchChoice.clear()
        for column in self.columns:
            self.searchChoice.addItem(column)

        # path to qpixmap inside cell
        photos = []
        for row in tableData:
            for column in self.columns:
                if rgx.search('photo', column):
                    pixmap = QPixmap(row[self.columns.index(column)])
                    photos.append(pixmap)

        model = TableModel(tableData, self.columns, photos)
        self.searchFilter.setSourceModel(model)
        self.table.setModel(model)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.resizeRowsToContents()
        self.table.setMinimumHeight(self.geometry().height() - 50) # do one more method for resizing

    def editRecord(self):
        row = self.table.currentIndex().row()
        if row == -1:
            return
        photos = []
        items = []
        for column in range(len(self.columns)):
            index = self.table.model().index(row, column)
            item = self.table.model().data(index, Qt.DisplayRole)
            image = self.table.model().data(index, Qt.DecorationRole)
            if item is not None:
                items.append(item)
            if image is not None:
                photos.append(image)

        editing = EditingWindow(self.controller, self.columns, items, photos, self.tableChoice.currentText())

        self.windowManager.addWidget(editing)
        self.windowManager.setCurrentWidget(editing)
        if editing.run():
            self.setTable()
            self.adjustSize()

        self.windowManager.setCurrentWidget(self)
