import configTools
import messageBoxes
from dotenv import get_key
import soundNotification
import HabrParser
import telegramBot


class HabrMyPostsBl():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HabrMyPostsBl, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        interval = self.get_interval()
        self.sound_Notification = soundNotification.get_sound_notification()  # чтобы каждый раз не лазить в ini
        self.tlg_notifications = configTools.get_tlg_notification()
        self.hp = HabrParser.HabrParser()       # инъекция парсера (((

    def get_interval(self):
        interval = configTools.get_interval()
        if interval == 0:  # что-то с конфигурационником
            if messageBoxes.show_message_dialog('Critical', get_key('my_env.env', 'ERROR_BAD_INI_FILE'), 'Внимание!'):
                configTools.create_new_config()
                interval = 3*1000*60
            else:
                exit(1)
        return interval*1000*60

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

    def setup_ini(self):
        self.sound_Notification = soundNotification.get_sound_notification()
        self.tlg_notifications = configTools.get_tlg_notification()
        return self.get_interval()
