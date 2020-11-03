import smtplib
import configparser
from AbstractAlarmNotification import AbstractAlarmNotification
"""""
 Шефф фсе пропало - на мыло 
 нужен файл private_set.ini - ессно он в .gitignore
"""""


class MailAlarmNotification(AbstractAlarmNotification):
    @staticmethod
    def alarm_notification(alarm_message):
        def read_ini():
            config = configparser.ConfigParser()
            config.read("private_set.ini")
            return {'smtp': config['Mail']['smtp'],
                    'smtp_port':  config['Mail']['smtp_port'],
                    'email': config['Mail']['email'],
                    'password': config['Mail']['password'], }

        mail_ini = read_ini()
        try:
            smtp_obj = smtplib.SMTP_SSL(mail_ini['smtp'], int(mail_ini['smtp_port']))
        except Exception as e:
            print(f'SMTP_SSL - problem {e}')
        smtp_obj.ehlo()
        smtp_obj.login(mail_ini['email'], mail_ini['password'])
        smtp_obj.sendmail(mail_ini['email'], mail_ini['email'], 'Subject: ' + alarm_message)
        smtp_obj.quit()
