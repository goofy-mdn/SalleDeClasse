import PySide2
from PySide2.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
import typing
import operator


class CustomTableModel(QAbstractTableModel):

    def __init__(self, parent, data_list, header):
        """
        Custom table model for the table view

        :param parent: parent table view object
        :type parent: QTableView
        :param data_list: list of objects to set in this model
        :type data_list: list
        :param header: column names
        :type header: tuple
        """
        QAbstractTableModel.__init__(self, parent)

        self.data_list = data_list
        self.header = header

        parent.setModel(self)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.data_list)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.header)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.data_list[index.row()][index.column()]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        return None

    def sort(self, column: int, order: PySide2.QtCore.Qt.SortOrder = ...):
        self.layoutAboutToBeChanged.emit()
        self.data_list = sorted(self.data_list, key=operator.itemgetter(column), reverse=order != Qt.AscendingOrder)
        self.layoutChanged.emit()
        self.parent().clearSelection()


class CustomTableView(QTableView):

    def __init__(self, single_selection: bool=True):
        """
        Common TableView used in side panels

        :param single_selection: disable multi-selection (True by default)
        :type single_selection: bool
        """
        QTableView.__init__(self)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection if single_selection else QAbstractItemView.MultiSelection)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
