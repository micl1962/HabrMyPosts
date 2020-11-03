from PyQt5 import QtCore, QtGui, QtWidgets
import os
from dotenv import get_key
import configTools
import appres
import soundNotification
import messageBoxes
"""
настройка аудио. Программной логики мало, в отдельный файл выделять смысла особого нет
"""


class SoundDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SoundDialog, self).__init__(parent)
        self.setObjectName("SnDialog")

        self.setFixedSize(400, 325)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # убираем ? из заголовка окна
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 280, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 20, 161, 16))
        self.label.setObjectName("label")
        # groupBox с радиокнопками и настройками
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 351, 211))
        self.groupBox.setObjectName("groupBox")
        self.radioButton_not = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_not.setGeometry(QtCore.QRect(20, 30, 93, 17))
        self.radioButton_not.setObjectName("radioButton_not")
        self.radioButton_beep = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_beep.setGeometry(QtCore.QRect(20, 70, 82, 17))
        self.radioButton_beep.setObjectName("radioButton_beep")
        self.radioButton_file = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_file.setGeometry(QtCore.QRect(20, 110, 82, 17))
        self.radioButton_file.setObjectName("radioButton_file")
        self.radioButton_text = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_text.setGeometry(QtCore.QRect(20, 150, 82, 17))
        self.radioButton_text.setObjectName("radioButton_text")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(130, 70, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(3)
        self.spinBox.setObjectName("spinBox")
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(110, 15, 20, 191))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.labelCountBeeps = QtWidgets.QLabel(self.groupBox)
        self.labelCountBeeps.setGeometry(QtCore.QRect(190, 70, 151, 16))
        self.labelCountBeeps.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(130, 110, 31, 23))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/OPEN.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.show_open_dialog)
        self.labelAudioFile = QtWidgets.QLabel(self.groupBox)
        self.labelAudioFile.setGeometry(QtCore.QRect(190, 110, 130, 16))
        self.labelAudioFile.setObjectName("label_3")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setGeometry(QtCore.QRect(130, 150, 201, 51))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.pushButtonTest = QtWidgets.QPushButton(self)
        self.pushButtonTest.setGeometry(QtCore.QRect(30, 250, 31, 23))
        self.pushButtonTest.setText("")
        _icon = QtGui.QIcon()
        _icon.addPixmap(QtGui.QPixmap(":/icon/sound.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonTest.setIcon(_icon)
        self.pushButtonTest.setObjectName("pushButtonTest")
        self.pushButtonTest.clicked.connect(self.select_for_sound_test)
        self.labelTestButton = QtWidgets.QLabel(self)
        self.labelTestButton.setGeometry(QtCore.QRect(70, 250, 140, 16))
        self.labelTestButton.setObjectName("label_4")
        self.fill_texts()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.plainTextEdit.textChanged.connect(self.set_current_text)
        self.spinBox.valueChanged.connect(self.set_current_beep_numbers)

    def set_current_text(self):
        self.rb_execute["radioButton_text"][1] = self.plainTextEdit.toPlainText()

    def set_current_beep_numbers(self):
        self.rb_execute["radioButton_beep"][1] = int(self.spinBox.value())

    def get_current_rb(self):
        rb_group_box = self.groupBox.findChildren(QtWidgets.QRadioButton)
        if rb_group_box is None:
            return None
        for rb in rb_group_box:
            if rb.isChecked():
                return rb
        return None

    # запускаемую функцию и ее параметр по активной р-баттон берем из self.rb_execute
    def select_for_sound_test(self):
        rb = self.get_current_rb()  # получаем тек активную р-баттон
        if rb is None:
            print('что-то пошло не так, нет текущей радиокнопки')
            return
        elif rb.objectName() == 'radioButton_not':
            return
        else:
            self.rb_execute[rb.objectName()][0](self.rb_execute[rb.objectName()][1])

    def fill_texts(self):
        self.setWindowTitle("Озвучивать свежий пост")
        self.label.setText("Как будете оповещать?")
        self.groupBox.setTitle("Варианты оповещения")
        self.radioButton_not.setText('Не оповещать')
        self.radioButton_beep.setText("Beep")
        self.radioButton_file.setText("Аудиофайл")
        self.radioButton_text.setText("Текст")
        audio = configTools.get_audio()  # выставляем параметры из .ini
        self.spinBox.setValue(int(audio['beep']))
        self.audioFile = audio['file']
        self.plainTextEdit.setPlainText(audio['text'])
        # привязка имени RB к функции и параметру для теста
        self.rb_execute = \
            {self.radioButton_beep.objectName(): [soundNotification.sound_beep, int(self.spinBox.value()), 'beep'],
             self.radioButton_file.objectName(): [soundNotification.sound_audio, self.audioFile, 'file'],
             self.radioButton_text.objectName(): [soundNotification.sound_text, self.plainTextEdit.toPlainText(), 'text'], }
    #  из ини активная радиобаттн
        if audio['current'] == '':
            self.radioButton_not.setChecked(True)
        else:
            for key in self.rb_execute:
                if self.rb_execute[key][2] == audio['current']:
                    rb_current = self.groupBox.findChild(QtWidgets.QRadioButton, key)
                    rb_current.setChecked(True)

        self.labelTestButton.setText('Тест выбранного варианта ')
        self.labelCountBeeps.setText("Количество сигналов")
        self.labelAudioFile.setText(os.path.basename(self.audioFile))

    def show_open_dialog(self):
        if self.audioFile == 'Файл не выбран':
            audio_file = './'
        else:
            audio_file = self.audioFile
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', audio_file, 'Audio Files(*.mp3 )')
        if file_name[1] == '':  # была отмена
            return
        self.labelAudioFile.setText(os.path.basename(file_name[0]))
        self.audioFile = file_name[0]
        self.rb_execute["radioButton_file"][1] = self.audioFile

    def accept(self):
        current_rb = self.get_current_rb()
        if current_rb.objectName() == 'radioButton_not':
            current_option = ''
        else:
            current_option = self.rb_execute[current_rb.objectName()][2]
        # установить
        audio_dict = configTools.get_audio()
        new_audio_dict = {'current': current_option,
                          'file': self.audioFile,
                          'beep': str(self.spinBox.value()),
                          'text': self.plainTextEdit.toPlainText(), }
        if new_audio_dict != audio_dict:
            messageBoxes.show_message_box('Information', get_key('my_env.env', 'NOTE_SAVE_SOUND_PARAM'), 'Информация!')
            configTools.set_audio(new_audio_dict)
            if current_option != '':  # параметры менялись - но если текущее не выставлено - ничего не сохраняем
                soundNotification.set_current_audio(current_option, self.rb_execute[current_rb.objectName()][1])

        self.hide()

    def reject(self) -> None:
        if messageBoxes.show_message_dialog('Warning', get_key('my_env.env', 'NOTE_NO_SAVE_SOUND_PARAM'), 'Внимание!'):
            self.hide()
