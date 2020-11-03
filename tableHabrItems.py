from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from toLink import openLink


class CreateTable(QTableWidget): 

    def __init__(self):
        super(CreateTable, self).__init__()
        self.setColumnCount(4)
        self.dictItemHeaders = {'Название статьи на Хабре': 0,
                                'теги': 1,
                                'Время': 2,
                                'Link': 3, }
        self.setHorizontalHeaderLabels(self.dictItemHeaders.keys())
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
        vh = self.verticalHeader()
        vh.setDefaultSectionSize(40)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.Stretch)
        self.setColumnHidden(3, True)

        # self.resizeColumnsToContents()
        self.setWordWrap(True)

        self.itemDoubleClicked.connect(self.item_choice)

    def addItems(self, list_items):
        for dictRow in reversed(list_items):
            self.insertRow(0)
            self.setItem(0, 0, QTableWidgetItem(dictRow['post_name']))
            self.setItem(0, 1, QTableWidgetItem(dictRow['str_post_tags']))
            self.setItem(0, 2, QTableWidgetItem(dictRow['post_date']))
            self.setItem(0, 3, QTableWidgetItem(dictRow['post_link']))

    def item_choice(self):
        link = self.item(self.currentRow(), 3).text()
        openLink(link)

    def __repr__(self):  # нужен был список айтемов таблицы
        sr = f'Class {self.__class__.__name__}\n***** Table content *****\n'
        sr += str([self.item(i, 0).text() for i in range(self.rowCount())])
        return sr
