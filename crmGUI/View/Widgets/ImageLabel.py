from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import hashlib


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        self.imagePath = ''

    def setPixmap(self, image):
        super().setPixmap(QPixmap(image))
        self.imagePath = image

    def text(self):
        return self.imagePath
