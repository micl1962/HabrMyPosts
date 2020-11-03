from PyQt5.QtWidgets import QMessageBox


def show_message(msg_box, type_message, content, win_title='', additional=''):
    type_messages_diction = {'Information': QMessageBox.Information,
                             'Warning': QMessageBox.Warning,
                             'Critical': QMessageBox.Critical, }
    if type_message in type_messages_diction:
        msg_box.setIcon(type_messages_diction[type_message])
    msg_box.setText(content)
    msg_box.setInformativeText(additional)
    msg_box.setWindowTitle(win_title)
    # msgBox.setDetailedText("The details are as follows:")


def show_message_box(type_message, content, win_title='', additional=''):
    msg_box = QMessageBox()
    show_message(msg_box, type_message, content, win_title, additional)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


# принимает тексты , возвращает if Ok -> True
def show_message_dialog(type_message, content, win_title='', additional='') -> bool:
    msg_box = QMessageBox()
    show_message(msg_box, type_message, content, win_title, additional)
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # return_value = msg_box.exec()
    return msg_box.exec() == QMessageBox.Ok
