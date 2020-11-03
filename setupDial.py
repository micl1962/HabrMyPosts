from PyQt5 import QtCore, QtWidgets
import configTools
import soundChoice
import appres    # resource file
from lib import setupDialBl
"""""
диалоговое окно
установить / редактировать параметры приложения
"""""


class SetupDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SetupDialog, self).__init__(parent)
        self.setObjectName("Dialog")

        self.setFixedSize(530, 550)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # убираем ? из заголовка окна

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(130, 510, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.listWidgetAllTags = QtWidgets.QListWidget(self)
        self.listWidgetAllTags.setGeometry(QtCore.QRect(20, 30, 220, 311))
        self.listWidgetAllTags.setObjectName("listWidgetAllTags")
        self.listWidgetMyTags = QtWidgets.QListWidget(self)
        self.listWidgetMyTags.setGeometry(QtCore.QRect(270, 30, 231, 311))
        self.listWidgetMyTags.setObjectName("listWidgetMyTags")

        self.labelAllTags = QtWidgets.QLabel(self)
        self.labelAllTags.setGeometry(QtCore.QRect(30, 10, 47, 13))
        self.labelAllTags.setObjectName("labelAllTags")
        self.labelMyTags = QtWidgets.QLabel(self)
        self.labelMyTags.setGeometry(QtCore.QRect(330, 10, 91, 16))
        self.labelMyTags.setObjectName("labelMyTags")
        self.labelDelTag = QtWidgets.QLabel(self)
        self.labelDelTag.setGeometry(QtCore.QRect(270, 340, 231, 16))
        self.labelDelTag.setObjectName("labelDelTag")
        self.labelAddTag = QtWidgets.QLabel(self)
        self.labelAddTag.setGeometry(QtCore.QRect(20, 340, 231, 16))
        self.labelAddTag.setObjectName("labelAddTag")

        self.labelScanPeriodicity = QtWidgets.QLabel(self)
        self.labelScanPeriodicity.setGeometry(QtCore.QRect(140, 380, 420, 13))
        self.labelScanPeriodicity.setObjectName("labelScanPeriodicity")

        self.comboB = QtWidgets.QComboBox(self)
        self.comboB.setGeometry(QtCore.QRect(20, 380, 100, 22))

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(20, 360, 420, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(240, 110, 30, 23))
        self.pushButton.setObjectName("pushButton")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(20, 410, 500, 95))
        self.groupBox.setObjectName("groupBox")
        self.labelSound = QtWidgets.QLabel(self.groupBox)
        self.labelSound.setGeometry(QtCore.QRect(10, 20, 190, 17))
        self.labelSound.setObjectName("labelSound")
        self.labelSoundCurrent = QtWidgets.QLabel(self.groupBox)
        self.labelSoundCurrent.setGeometry(QtCore.QRect(290, 23, 190, 17))
        self.labelSoundCurrent.setObjectName("labelSoundCurrent")

        self.pushButtonSound = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonSound.setGeometry(QtCore.QRect(190, 20, 90, 23))
        self.pushButtonSound.setObjectName("pushButtonSound")

        self.checkBoxTlg = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxTlg.setGeometry(QtCore.QRect(10, 40, 300, 40))
        self.checkBoxTlg.setObjectName("checkBoxTlg")
        self.pushButton.clicked.connect(self.choice_item)
        self.listWidgetAllTags.itemDoubleClicked.connect(self.choice_item)
        self.listWidgetMyTags.itemDoubleClicked.connect(self.delete_item)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.pushButtonSound.clicked.connect(self.sound_set)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.fill_wigets()
        self.fill_settings()     # из settings.ini заполняем ранее выбранные теги

    def fill_wigets(self):
        self.setWindowTitle("Setup")
        self.labelAllTags.setText("Все Тэги")
        self.labelMyTags.setText("Выбранные тэги")
        self.labelDelTag.setText("Двойной клик - удалить из выбр.тэгов")
        self.labelAddTag.setText("Двойной клик - выбрать тэг")
        self.labelScanPeriodicity.setText("Укажите интервал (мин.) частоты сканирования Хабра")
        self.pushButton.setText("->")
        self.groupBox.setTitle("Доп. настройки")
        self.labelSound.setText("Озвучивать свежий пост")
        self.checkBoxTlg.setText\
            ("Уведомлять Телеграм-ботом - необходио указать\napi токен ( параметр в private_set.ini )")
        self.pushButtonSound.setText("Настроить")

    def fill_settings(self):
        # все теги
        tags = QtCore.QFile("://textTags/tagsutf8.txt")
        source = 'Ошибка загрузки тегов'
        try:
            tags.open(QtCore.QFile.ReadOnly)
            source = bytes(tags.readAll()).decode('utf-8')
        except Exception as e:
            print(e)

        tags_list = [item.strip() for item in source.split('\n')]
        self.listWidgetAllTags.addItems(tags_list)
        self.listWidgetAllTags.setCurrentRow(0)
        # выбранные теги
        choice_tags = list(configTools.get_elected_tags())
        if choice_tags != ['']:
            choice_tags.sort()
            self.listWidgetMyTags.addItems(choice_tags)
        # временной интервал сканирования
        interval, scan_interval = setupDialBl.get_interval_info()
        for i in range(1, scan_interval, 1):
            self.comboB.addItem(str(i))
        self.comboB.setCurrentIndex(interval-1)
        # аудио
        self.sound_active_view()
        # tlg
        self.checkBoxTlg.setChecked(configTools.get_tlg_notification())

    def choice_item(self):
        if setupDialBl.choice_item(self.listWidgetAllTags.currentItem().text(), self.my_items_list()):
            self.listWidgetMyTags.addItem(self.listWidgetAllTags.currentItem().text())

    def delete_item(self):
        list_items = self.listWidgetMyTags.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listWidgetMyTags.takeItem(self.listWidgetMyTags.row(item))

    def sound_set(self):
        dialog = soundChoice.SoundDialog(self)
        dialog.exec_()
        self.sound_active_view()

    def sound_active_view(self):
        self.labelSoundCurrent.setText(setupDialBl.sound_active_view())

    def reject(self) -> None:
        if not setupDialBl.no_items(self.my_items_list()):
            self.hide()

    def accept(self):
        setupDialBl.accept(self.my_items_list(), self.checkBoxTlg.isChecked(), self.comboB.currentText())
        self.hide()

    def my_items_list(self):
        return [str(self.listWidgetMyTags.item(i).text()) for i in range(self.listWidgetMyTags.count())]


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = SetupDialog()
    ex.exec_()
