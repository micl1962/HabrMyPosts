import pathlib
import pyttsx3
from PyQt5.QtCore import QFile
import shutil
from playsound import playsound
import appres  # ресурсы
import configTools

audio_files =\
    {'beep': '.\\media\\many_beeps.mp3', 'text': '.\\media\\text_audio.wav', 'file': '.\\media\\file_audio.mp3'}


def create_beep(beep_count, beep_notif):
    one_beep_tmp = '.\\media\\beep-01.mp3'
    if pathlib.Path(beep_notif).exists():
        pathlib.Path(beep_notif).unlink()
    if not pathlib.Path(one_beep_tmp).exists():
        beep = QFile("://audio/beep-01a.mp3")
        QFile.copy(beep.fileName(), one_beep_tmp)
    destination = open(beep_notif, 'wb')
    for i in range(1, beep_count + 1):
        beep_tmp = open(one_beep_tmp, 'rb')
        shutil.copyfileobj(beep_tmp, destination)
        beep_tmp.close()
    destination.close()
    pathlib.Path(one_beep_tmp).chmod(33206)
    pathlib.Path(one_beep_tmp).unlink()


def sound_beep(beep_count):
    create_beep(beep_count, audio_files['beep'])
    sound_audio(audio_files['beep'])


def sound_audio(file_name):
    if pathlib.Path(file_name).exists():
        playsound(file_name)


def create_file(file_name, file_notif):
    if pathlib.Path(file_notif).exists():
        pathlib.Path(file_notif).unlink()
    if not pathlib.Path(file_name).exists():
        return
    shutil.copy(file_name, file_notif)


def sound_text(text):
    text_notif = audio_files['text']
    create_text(text, text_notif, False)
    # sound_audio(text_notif)


def create_text(text, text_notif, for_save=True):
    if text.strip() == '':
        return
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male 1 for femal
    if for_save:
        if pathlib.Path(text_notif).exists():
            is_free = False
            while not is_free:
                try:
                    pathlib.Path(text_notif).unlink()
                    is_free = True
                except OSError as e:
                    print(f'Permission error {e}')
                    return
        engine.save_to_file(text, text_notif)
    else:
        engine.say(text)
    engine.runAndWait()
    engine.stop()


# готовит аудиофайл для выбранной опции
def set_current_audio(current_audio, param):
    sound_dict = {'beep': create_beep, 'text': create_text, 'file': create_file}
    current_option = sound_dict.get(current_audio)
    if current_option is not None:
        current_option(param, audio_files.get(current_audio))


def get_sound_notification():
    audio = configTools.get_audio()
    file_name = get_file_name(audio['current'])
    if file_name is None:
        return None

    def wrap():
        sound_audio(file_name)
    return wrap


# проверка текущего для воспр. файла -  если тип не из списка или сам файл не существует - верноуть None
def get_file_name(current_audio):
    file_name = audio_files.get(current_audio)
    if file_name is None or not pathlib.Path(file_name).exists():
        return None

    return file_name
