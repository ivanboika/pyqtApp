from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class AddRecord(QDialog):
    def __init__(self, daoObject, columns):
        super().__init__()

        self.setWindowTitle('Добавление записи')

        self.daoObject = daoObject
        okButton = QPushButton('Добавить')
        cancelButton = QPushButton('Отмена')

        self.addLayout = QGridLayout()
        self.addLayout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.addLayout)

        temp = 0
        for column in columns:
            self.addLayout.addWidget(QLabel(column), temp, 0)
            textEdit = QLineEdit()
            self.addLayout.addWidget(textEdit, temp, 1)
            temp += 1

        self.addLayout.addWidget(okButton, temp, 0)
        self.addLayout.addWidget(cancelButton, temp, 1)

        okButton.clicked.connect(self.addButtonOkButtonClicked)
        cancelButton.clicked.connect(self.close)

    def addButtonOkButtonClicked(self):
        partQuery = ''
