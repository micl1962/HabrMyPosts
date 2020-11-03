from abc import ABCMeta
"""""
 если - Шефф фсе пропало - куда посылать весточку; писать наследника, в нем свой метод alarm_notification
 в модуле, где используется, менять только импорт
"""""


class AbstractAlarmNotification(metaclass=ABCMeta):
    @staticmethod
    def alarm_notification(alarm_message):
        return
