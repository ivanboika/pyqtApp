from src.View.ImageLabel import ImageLabel
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt

from src.Model.ModelHandler import modelHandler
from src.Model.BaseModel import Base
import regex as rgx


class EditingWindow(QDialog):
    def __init__(self, connectionObject, columnNames, items: list, photos: list, table):
        super(EditingWindow, self).__init__()

        self.setAcceptDrops(True)

        self.setWindowTitle('Редактирование записи')

        self.mainLayout = QGridLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.image = ImageLabel()
        self.status = False
        self.columnNames = columnNames
        self.controller = connectionObject
        self.table = table

        okButton = QPushButton('Добавить')
        cancelButton = QPushButton('Отмена')

        temp = 0
        photoIndex = 0
        itemIndex = 0
        for column in columnNames:
            self.mainLayout.addWidget(QLabel(column), temp, 0)
            if rgx.search('photo', column):
                self.photoViewer = ImageLabel()
                self.photoViewer.setPixmap(photos[photoIndex])
                self.mainLayout.addWidget(self.photoViewer, temp, 1)
                photoIndex += 1
            else:
                textEdit = QLineEdit()
                textEdit.setText(str(items[itemIndex]))
                self.mainLayout.addWidget(textEdit, temp, 1)
                itemIndex += 1
            temp += 1

        self.mainLayout.addWidget(okButton, temp, 0)
        self.mainLayout.addWidget(cancelButton, temp, 1)
        self.setLayout(self.mainLayout)

        okButton.clicked.connect(self.addButtonOkButtonClicked)
        cancelButton.clicked.connect(self.close)

    def addButtonOkButtonClicked(self):
        values = {}
        for row in range(self.mainLayout.rowCount() - 1):
            values.update({self.columnNames[row]: self.mainLayout.itemAtPosition(row, 1).widget().text()})
        self.controller.updateRecord(modelHandler(self.table), values)

        self.status = True
        self.close()

    def run(self):
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