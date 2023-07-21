from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class AddRecord(QDialog):
    def __init__(self, daoObject, columns, tableName):
        super().__init__()

        self.setWindowTitle('Добавление записи')

        self.daoObject = daoObject
        self.tableName = tableName
        self.columnNames = columns
        self.status = False

        okButton = QPushButton('Добавить')
        cancelButton = QPushButton('Отмена')

        self.addLayout = QGridLayout()
        self.addLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.addLayout)

        temp = 0
        for column in columns:
            self.addLayout.addWidget(QLabel(column), temp, 0)
            textEdit = QLineEdit()
            self.addLayout.addWidget(textEdit, temp, 1)
            temp += 1

        self.addLayout.addWidget(okButton, temp, 0)
        self.addLayout.addWidget(cancelButton, temp, 1)

        self.adjustSize()
        okButton.clicked.connect(self.addButtonOkButtonClicked)
        cancelButton.clicked.connect(self.close)

    def addButtonOkButtonClicked(self):
        query = 'INSERT INTO ' + self.tableName + '('

        for index in range(len(self.columnNames)):
            query += self.columnNames[index] + ','
        query = query.removesuffix(',')
        query += ') VALUES ('

        columnValues = []

        for row in range(self.addLayout.rowCount() - 1):
            columnValues.append(self.addLayout.itemAtPosition(row, 1).widget().text())

        for index in range(len(columnValues)):
            query += '\'' + columnValues[index] + '\','
        query = query.removesuffix(',')
        query += ');'
        self.daoObject.exec(query)
        self.status = True
        self.close()

    def run(self) -> bool:
        self.exec_()
        return self.status
