from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QGridLayout, QLineEdit

import regex as rgx

from crmGUI.View.Widgets.ImageLabel import ImageLabel
from crmGUI.Model.ModelHandler import modelHandler


class AddRecord(QDialog):
    def __init__(self, connectionObject, columns, tableName):
        super().__init__()

        self.setAcceptDrops(True)

        self.setWindowTitle('Добавление записи')

        self.connectionObject = connectionObject
        self.tableName = tableName
        self.columnNames = columns
        self.filePath = ''
        self.status = False

        okButton = QPushButton('Добавить')
        cancelButton = QPushButton('Отмена')

        self.addLayout = QGridLayout()
        self.addLayout.setAlignment(Qt.AlignTop)

        temp = 0
        for column in columns:
            self.addLayout.addWidget(QLabel(column), temp, 0)
            if rgx.search('photo', column):
                self.photoViewer = ImageLabel()
                self.addLayout.addWidget(self.photoViewer, temp, 1)
            else:
                textEdit = QLineEdit()
                self.addLayout.addWidget(textEdit, temp, 1)
            temp += 1

        self.addLayout.addWidget(okButton, temp, 0)
        self.addLayout.addWidget(cancelButton, temp, 1)
        self.setLayout(self.addLayout)

        self.adjustSize()
        okButton.clicked.connect(self.addButtonOkButtonClicked)
        cancelButton.clicked.connect(self.close)

    def addButtonOkButtonClicked(self):
        values = {}

        for row in range(self.addLayout.rowCount() - 1):
            values.update({self.columnNames[row]: self.addLayout.itemAtPosition(row, 1).widget().text()})

        self.connectionObject.insertRecord(modelHandler(self.tableName), values)

        self.status = True
        self.close()

    def run(self) -> bool:
        self.exec_()
        return self.status

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.filePath = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.filePath)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(file_path)
