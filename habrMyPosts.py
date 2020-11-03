from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QMenu, QAction, QStyle, qApp, QPushButton, QLabel
from PyQt5.QtCore import QSize, QTimer
import tableHabrItems
import configTools
import soundNotification
from lib import HabrMyPostsBl
import setupDial


"""""
    класс - создаст главное окно , подтянет зависимости (парсинг, дататейбл), покажет найденные по тэгам посты,
    по желанию пользователя свернет приложение в трей
"""""


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.timer = QTimer(self)
        self.habr_posts_model = HabrMyPostsBl.HabrMyPostsBl()
        interval = self.habr_posts_model.get_interval()
        self.timer.setInterval(interval)
        self.sound_Notification = soundNotification.get_sound_notification()  # чтобы каждый раз не лазить в ini
        self.tlg_notifications = configTools.get_tlg_notification()
        self.timer.timeout.connect(self.check_new_posts)

        self.setMinimumSize(QSize(640, 280))
        main_window_size = self.habr_posts_model.get_main_window_size()
        self.resize(main_window_size['width'], main_window_size['height'])
        self.setWindowTitle("Long Live Habr!!!")
        self.statusBar().addPermanentWidget(QLabel(f'Установлен интервал сканирования: {int(interval/(1000*60))} мин.         '))
        # self.statusBar().addPermanentWidget(QWidget())
        self.statusBar().addPermanentWidget(QLabel('Двойной клик откроет статью в вашем браузере по умолчаню'))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(central_widget)

        # self.hp = HabrParser.HabrParser()       # инъекция парсера (((
        self.table = tableHabrItems.CreateTable()
        grid_layout.addWidget(self.table, 1, 0, 1, 4)   # Добавляем таблицу в сетку
        self.checkBox = QCheckBox('При закрытии окна остаться в трее')
        grid_layout.addWidget(self.checkBox, 2, 0)

        self.pushButtonSetup = QPushButton('Настройки')
        self.pushButtonSetup.clicked.connect(self.open_setup_dialog)
        grid_layout.addWidget(self.pushButtonSetup, 3, 3)

    # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show_main_window)
        quit_action.triggered.connect(self.close_app)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip('Habr scanning\nActions - RBM')

    def show_main_window(self):
        main_window_size = self.habr_posts_model.get_main_window_size()
        self.resize(main_window_size['width'], main_window_size['height'])

        self.tray_icon.hide()
        self.show()

    def close_app(self):
        self.tray_icon.hide()
        qApp.quit()

    # перехват события закрытия главного окна
    def closeEvent(self, event):
        configTools.set_main_window_size({'width': self.width(), 'height': self.height()})
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))

        if self.checkBox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.show()
        else:
            self.tray_icon.hide()

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def check_new_posts(self):
        if self.habr_posts_model.check_new_posts(self.table):
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_DialogHelpButton))

    def open_setup_dialog(self):
        self.stop()
        dialog = setupDial.SetupDialog(self)
        dialog.exec_()
        interval = self.habr_posts_model.setup_ini()
        self.timer.setInterval(interval)
        self.start()


def main():
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.check_new_posts()
    main_window.show()
    main_window.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
else:
    print(__name__)
