import configparser
import telegramBot
"""
Вернет-запишет параметры из settings.ini
"""
config = configparser.ConfigParser()


def get_elected_tags() -> set:
    config.read("settings.ini")
    set_items = set(config['Tags']['Items'].split(','))

    return set_items


def set_elected_tags(list_items):
    config.read("settings.ini")
    config['Tags']['items'] = list_items
    with open('settings.ini', 'w') as conf:
        config.write(conf)


def get_interval() -> int:
    x = config.read("settings.ini")
    if len(x) == 0:
        return 0
    interval = config['Interval']['items']
    if not interval.isdigit() or int(interval) not in [1, 61]:
        config['Interval']['items'] = '3'
        with open('settings.ini', 'w') as conf:
            config.write(conf)
        interval = '3'
    return int(interval)


def set_interval(interval: str):
    config.read("settings.ini")
    if config['Interval']['items'] != interval:
        config['Interval'] = {'items' : interval}
        with open('settings.ini', 'w') as conf:
            config.write(conf)


def get_main_window_size():
    x = config.read("settings.ini")
    if len(x) == 0:
        return {}
    return config._sections['MainWindowSize']


def set_main_window_size(main_window_size: dict):
    config.read("settings.ini")
    config['MainWindowSize'] = main_window_size
    with open('settings.ini', 'w') as conf:
        config.write(conf)


# def getMyTagsSet() -> set:
#     config.read("settings.ini")
#     return set(config['Tags']['items'].split(','))


def create_new_config():
    config['MainWindowSize'] = {'items': '800,600'}
    config['Tags'] = {'items' : 'Java,Python'}
    config['Interval'] = {'items' : '3'}
    config['AudioFile'] = {'current': '', 'file': '', 'beep': '2', 'text': 'Привет, Хабр!'}
    config['Tlg'] = {'notification': 'True'}

    with open('settings.ini', 'w') as conf:
        config.write(conf)


# def setAudioFile(filename):
#     config.read("settings.ini")
#     config['AudioFile']['file'] = filename
#
#     with open('settings.ini', 'w') as conf:
#         config.write(conf)


def get_audio() -> dict:
    config.read("settings.ini")

    return config._sections['AudioFile']


# что приятно - функцию не придется менять при колич/кач изменении параметров аудио
def set_audio(audio_params: dict):
    config.read("settings.ini")
    config['AudioFile'] = audio_params

    with open('settings.ini', 'w') as conf:
        config.write(conf)


def get_tlg_notification() -> bool:
    config.read("settings.ini")
    if config['Tlg']['notification'] == 'True':
        if telegramBot.get_ini_tlg() is not None:
            return True
    return False


def set_tlg_notification(tlg_notification):
    config.read("settings.ini")
    config['Tlg']['notification'] = tlg_notification
    with open('settings.ini', 'w') as conf:
        config.write(conf)
