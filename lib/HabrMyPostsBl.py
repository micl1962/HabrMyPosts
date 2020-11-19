from dotenv import get_key
import configTools
import messageBoxes
import soundNotification
import HabrParser
import telegramBot as telegramBot
import setupDial


class HabrMyPostsBl():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HabrMyPostsBl, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not configTools.check_cfg(configTools.cfg_file):
            if messageBoxes.show_message_dialog('Critical', ' Файл settings.ini не найден или поврежден!\n'
                                                            'Желаете его создать?\n'
                                                            'Отказ - выход из программы', 'Внимание!'):
                configTools.create_new_config()
            else:
                exit(1)
        self.sound_Notification = soundNotification.get_sound_notification()  # чтобы каждый раз не лазить в ini
        self.tlg_notifications = configTools.get_tlg_notification()
        self.hp = HabrParser.HabrParser()       # инъекция парсера (((

    def get_interval(self):
        interval = configTools.get_interval()
        if interval is None:  # в конфигурационнике отсутствует поле для интервала
            interval = 3
        return interval

    def get_main_window_size(self):
        main_window_size = configTools.get_main_window_size()
        return {'width': int(main_window_size['width']),'height': int(main_window_size['height'])}

    def check_new_posts(self, table) -> bool:
        all_posts = self.hp.postRequest()
        if len(all_posts) > 0:
            table.addItems(all_posts)
            if self.tlg_notifications:
                telegramBot.tlg_notification(all_posts)
            if self.sound_Notification is not None:
                self.sound_Notification()
            return True
        return False

    def setup_dialog(self, param):
        dialog = setupDial.SetupDialog(param)
        dialog.exec_()
        self.sound_Notification = soundNotification.get_sound_notification()
        self.tlg_notifications = configTools.get_tlg_notification()

