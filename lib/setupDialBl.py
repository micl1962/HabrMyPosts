from dotenv import get_key
from telegramBot import get_ini_tlg
import configTools
import messageBoxes


def get_interval_info():
    scan_interval = int(get_key(configTools.get_env_name(), 'SCAN_INTERVAL_MAX')) + 1
    interval = configTools.get_interval()
    if interval not in range(1, scan_interval):
        interval = 3
    return interval, scan_interval


def sound_active_view() -> str:
    audio = configTools.get_audio()
    lau = list(audio.keys())
    lau.remove('current')
    if audio['current'] in lau:
        return 'Текущее ' + audio['current']
    return 'Неактивно'


def choice_item(all_tags_current: str, list_widget_my_tags: list):
    if all_tags_current not in list_widget_my_tags:
        list_widget_my_tags.append(all_tags_current)
        return True
    return False


def no_items(my_tags_list: list) -> bool:
    if len(my_tags_list) == 0:
        return messageBoxes.show_message_dialog('Critical', get_key(configTools.get_env_name(), 'NOTE_SETUP_EMPTY'),
                                                'Внимание!')

    return False


def accept(my_tags_list: list, check_box_tlg_is_checked: bool, interval: str):
    if no_items(my_tags_list):  # если подтв выход скрываем диал, если кансел остаемся редактировать
        return

    if check_box_tlg_is_checked:
        if get_ini_tlg() is None:
            messageBoxes.show_message_box('Warning', get_key(configTools.get_env_name(), 'NOTE_TLG_NOT_SET'),
                                          'Внимание!')
            configTools.set_tlg_notification('False')
        else:
            configTools.set_tlg_notification('True')
    else:
        configTools.set_tlg_notification('False')

    # тэги непусты, проверяем, менялись ли ?
    before_dial_my_items = configTools.get_elected_tags()
    tags_for_save = set(my_tags_list)

    if before_dial_my_items != tags_for_save:
        messageBoxes.show_message_box('Warning', get_key(configTools.get_env_name(), 'NOTE_TAGS_CHANGED'), 'Внимание!')
        configTools.set_elected_tags(','.join(my_tags_list))
    configTools.set_interval(interval)
