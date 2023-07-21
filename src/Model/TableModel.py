from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers, photos):
        super(TableModel, self).__init__()
        self._data = data
        self.headers = headers
        self.photos = photos

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return self.headers[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self, p_int, Qt_Orientation, role)

    def data(self, index, role):
        if role == Qt.DecorationRole and len(self.photos) and self.headers[index.column()] == 'photo':
            return self.photos[index.row()]

        if role == Qt.SizeHintRole and len(self.photos) and self.headers[index.column()] == 'photo':
            return self.photos[index.row()].size()

        if role == Qt.DisplayRole and self.headers[index.column()] != 'photo':
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
