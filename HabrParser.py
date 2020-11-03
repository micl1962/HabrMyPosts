import requests
import bs4
from datetime import datetime, timedelta
from time import sleep
from dotenv import get_key
import configTools
import myLog
from AbstractHabrScan import AbstractHabrScan
# менять from, import для другого типа оповещения; алиас сохранить - и тело класса можно не трогать!
from mailAlarmNotification import MailAlarmNotification as AlarmNotification

logger = myLog.set_logs(__name__, 'habrParser')  # инит 2 журнала логов - общий и ошибки


class HabrParser(AbstractHabrScan):
    """""
    вернет лист dict-ов пересекающихся по тэгам постов более свежей даты чем self.lastDate c https://habr.com/ru/all/
    для перестраховки выбираю для инициализации дату позавчера, хотя совершенно не представляю
    такого редкого обновления статей на хабре - раненько утром только присутствуют 'вчера'
    формат листов возвращаемого листа
    {название статьи, тэги(str), дата публикации в честном формате, линк статьи(в таблице будет скрыт)}
    """""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HabrParser, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._lastPostName = ''
        self._lastPostDate = datetime.now() - timedelta(days=2)
        self._myTagsSet = configTools.get_elected_tags()
        self._month_list = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    def postRequest(self) -> list:
        posts_all_info_list = []
        # если время 00:00:00 сайт не успевает исправить свои сегодня/завтра
        dt_now = datetime.now()
        if dt_now.hour == 0 and dt_now.minute < 1 and dt_now.second < 59:
            sleep(60 - dt_now.second)

        try:
            res = requests.get(get_key('my_env.env', 'HABR_RU_ALL_URL'))
        except requests.exceptions.RequestException as e:
            logger.error("ConnectionError")
            logger.error(e)
            AlarmNotification.alarm_notification("ConnectionError " + datetime.now().strftime('%d-%b %H:%M'))
            return posts_all_info_list

        res.raise_for_status()
        html_data = bs4.BeautifulSoup(res.text, 'html.parser')
        finded_posts = html_data.find_all(class_='post')

        count = 0
        lastPostDateTmp = self._lastPostDate
        lastPostNameTmp = self._lastPostName
        logger.info('начиная с даты ' + self._lastPostDate.strftime('%d-%b %H:%M'))

        for paragraph in finded_posts:
            post_date_class = paragraph.find(class_='post__time')
            if post_date_class is None:  # в страницу вставили всякую хрень, это не пост, игнорируем
                continue
            else:
                pCont = post_date_class.contents
                # print(pCont)
                # post_date = self.postDateTime(post_date_class.text)
                post_date = self.post_date_time(pCont[0])
                if post_date < lastPostDateTmp:  # дата самого свежего поста < даты последней обработки
                    logger.error('********что-то пошло не так******* ')
                    logger.error(f'self.lastPostDate {self._lastPostDate.strftime("%d-%b %H:%M")}')
                    logger.error(f'lastPostDateTmp {lastPostDateTmp.strftime("%d-%b %H:%M")}')
                    logger.error(f'post_date {post_date.strftime("%d-%b %H:%M")}')
                    logger.error(f'count {count}')
                    post_attr = paragraph.find(class_='post__title_link')
                    logger.error(f'Название  непонятной статьи {post_attr.text}')
                    for item in posts_all_info_list:
                        logger.error(item)
                    return posts_all_info_list  # что-то произошло на странице - вверху оказалась старая дата

            post_attr = paragraph.find(class_='post__title_link')
            post_name = post_attr.text
            if count == 0:
                if post_date < self._lastPostDate:
                    logger.error('сразу дата поста меньше уже обработанных')
                    logger.error(f'lastPostDate {self._lastPostDate.strftime("%d-%b %H:%M")}')
                    logger.error(f'post_date {post_date.strftime("%d-%b %H:%M")}')
                    return posts_all_info_list
                # в переменные класса вносим дату и название самого свежего поста на данный момент
                self._lastPostDate = post_date
                self._lastPostName = post_name
                count = 1

            if post_date <= lastPostDateTmp and post_name == lastPostNameTmp:  # добрались до обработанных ранее записей
                break
            post_link = post_attr.get('href')
            str_post_tags = ''
            post_all_tags = paragraph.findChildren(class_='inline-list__item')
            set_post_tags = set()
            for tag_one in post_all_tags:
                try:
                    tag_item = (tag_one.find(class_='inline-list__item-link')).text
                except AttributeError:
                    logger.info(f'Tags AttributeError {post_name}')
                    continue
                str_post_tags += tag_item + ';'
                set_post_tags.add(tag_item)

            if len(self._myTagsSet.intersection(set_post_tags)) > 0:  # выбираем нужные статьи по тэгам
                _post_all_info = {'post_name': post_name,
                                  'str_post_tags': str_post_tags,
                                  'post_date': post_date.strftime('%d-%b %H:%M'),
                                  'post_link': post_link, }
                posts_all_info_list.append(_post_all_info)

        logger.info(f'Добавили {str(len(posts_all_info_list))} строк')
        logger.info(f'по дату {self._lastPostDate.strftime("%d-%b %H:%M")}')
        return posts_all_info_list

    def post_date_time(self, post_time) -> datetime:  # получаем из хабровской обычную дату
        def get_time(str_time):
            tmp = str_time.split(':')
            return int(tmp[0]), int(tmp[1])

        list_date_time = post_time.split(' ')
        dt_now = datetime.now()
        if 'сегодня' in list_date_time:
            a_hour, a_minute = get_time(list_date_time[2])
            dt = dt_now.replace(hour=a_hour, minute=a_minute, second=0, microsecond=0)
        elif 'вчера' in list_date_time:
            a_hour, a_minute = get_time(list_date_time[2])
            yesterday = dt_now - timedelta(days=1)
            dt = yesterday.replace(hour=a_hour, minute=a_minute, second=0, microsecond=0)
        else:
            mon = self._month_list.index(list_date_time[1])
            dt = datetime.strptime(
                list_date_time[0] + ' ' + str(mon) + ' ' + list_date_time[2] + ' ' + list_date_time[4] + ':00',
                '%d %m %Y %H:%M:%S')
        return dt
