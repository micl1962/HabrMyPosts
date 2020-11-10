import configparser
import pathlib
import telegramBot
"""
Вернет-запишет параметры из settings.ini
"""
config = configparser.ConfigParser()
cfg_file = "settings.ini"
# связь функции с _sections
function_section = {'get_elected_tags': 'Tags',
                    'get_interval': 'Interval',
                    'get_main_window_size': 'MainWindowSize',
                    'get_audio': 'AudioFile',
                    'get_tlg_notification': 'Tlg',
                    'get_env_name': 'Env', }


# декоратор на чтение
def read_cfg(func):
    def wrapper():
        if check_cfg(config.read(cfg_file)) and func.__name__ in function_section.keys():
            try:
                sec_content = config._sections[function_section.get(func.__name__)]
            except KeyError:
                     return None
            return func()
        return None
    return wrapper


# декоратор на запись
def write_cfg(func):
    def wrapper(*args):
        if check_cfg(config.read(cfg_file)):
            func(*args)
            with open(cfg_file, 'w') as conf:
                config.write(conf)
        return None
    return wrapper


@read_cfg
def get_elected_tags() -> set:
    return set(config['Tags']['Items'].split(','))


@write_cfg
def set_elected_tags(list_items):
    config['Tags']['items'] = list_items


@read_cfg
def get_interval() -> int:
    interval = config['Interval']['items']
    if not interval.isdigit() or int(interval) not in range(1, 61):
        interval = '3'
    return int(interval)


@write_cfg
def set_interval(interval: str):
    config['Interval'] = {'items': interval}


@read_cfg
def get_main_window_size():
    return config._sections['MainWindowSize']


@write_cfg
def set_main_window_size(main_window_size: dict):
    config['MainWindowSize'] = main_window_size


@read_cfg
def get_audio() -> dict:
    return config._sections['AudioFile']


# что приятно - функцию не придется менять при колич/кач изменении параметров аудио
@write_cfg
def set_audio(audio_params: dict):
    config['AudioFile'] = audio_params


@read_cfg
def get_tlg_notification() -> bool:
    if config['Tlg']['notification'] == 'True' and telegramBot.get_ini_tlg() is not None:
        return True
    return False


@write_cfg
def set_tlg_notification(tlg_notification):
    config['Tlg']['notification'] = tlg_notification


@read_cfg
def get_env_name() -> str:
    return config['Env']['file']


# def get_section_cfg(section_name) -> dict:
#     config.read(cfg_file)
#     try:
#         sec_content = config._sections[section_name]
#     except KeyError:
#         return None
#     return sec_content
#
#
# def set_section_cfg(section_name, items: dict):
#     config.read(cfg_file)
#     config[section_name] = items
#
#     with open(cfg_file, 'w') as conf:
#         config.write(conf)


def check_cfg(cfg_files_list):
    if not pathlib.Path(cfg_file).exists() or len(cfg_files_list) == 0:
        return False
    return True


@write_cfg
def create_new_config():
    config['MainWindowSize'] = {'items': '800,600'}
    config['Tags'] = {'items': 'Java,Python'}
    config['Interval'] = {'items': '3'}
    config['AudioFile'] = {'current': '', 'file': '', 'beep': '2', 'text': 'Привет, Хабр!'}
    config['Tlg'] = {'notification': 'True'}
    config['Env'] = {'file': 'my_env.env'}
