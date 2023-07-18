from PyQt5.QtWidgets import *
from src.Connection import DAO
from win32api import GetSystemMetrics
from src.TableModel import TableModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Application')
        self.setGeometry(0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

        self.dao = DAO()
        self.columns = []

        self.table = QTableView(self)
        self.tableChoice = QComboBox(self)
        self.widgetLayout = QWidget(self)

        self.addButton = QPushButton('Add record')
        self.editButton = QPushButton('Edit record')

        self.UI()

        self.tableChoice.currentIndexChanged.connect(self.itemChanged)
        self.addButton.clicked.connect(self.addButtonClicked)

    def UI(self):
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.addButton, 0, 0)
        buttonLayout.addWidget(self.editButton, 1, 0)
        buttonLayout.addWidget(self.tableChoice, 3, 0)
        buttonLayout.addWidget(QPushButton('Searching record'), 2, 0)
        buttonLayout.addWidget(self.table, 0, 1, 8, 8, Qt.AlignTop)
        buttonLayout.setAlignment(Qt.AlignLeft)

        self.widgetLayout.setLayout(buttonLayout)
        self.widgetLayout.adjustSize()
        self.setCentralWidget(self.widgetLayout)

        self.dao.exec("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema = 'public'""")

        for tableName in self.dao.getFromSelect():
            self.tableChoice.addItem(tableName[0])

        self.setTable()

    def itemChanged(self):
        self.setTable()

    def addButtonClicked(self):
        dialogWin = QDialog()
        dialogWin.setWindowTitle('Adding window')

        okButton = QPushButton('Ok')
        cancelButton = QPushButton('Cancel')

        addLayout = QGridLayout(dialogWin)
        addLayout.setAlignment(Qt.AlignLeft)
        dialogWin.setLayout(addLayout)

        temp = 0
        for column in self.columns:
            addLayout.addWidget(QLabel(column), temp, 0)
            textEdit = QLineEdit()
            addLayout.addWidget(textEdit, temp, 1)
            temp += 1

        addLayout.addWidget(okButton, temp, 0)
        addLayout.addWidget(cancelButton, temp, 1)

        okButton.clicked.connect(self.addButtonOkButtonClicked)
        cancelButton.clicked.connect(dialogWin.close)
        dialogWin.exec()

    def setTable(self):
        self.dao.exec('SELECT * FROM ' +
                      self.tableChoice.itemText(self.tableChoice.currentIndex()))

        data = self.dao.getFromSelect()
        self.columns = self.dao.getColumnNames(self.tableChoice.itemText(self.tableChoice.currentIndex()))

        # memoryview to qpixmap inside cell
        photos = []
        for row in data:
            for field in row:
                if type(field) is memoryview:
                    pixmap = QPixmap()
                    pixmap.loadFromData(field)
                    photos.append(pixmap)

        model = TableModel(data, self.columns, photos)
        self.table.setModel(model)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        self.table.resize(600, 400)

    def addButtonOkButtonClicked(self):
        #slot for pushing btn ok when adding a record
        self.dao.exec()