import logging
from dotenv import get_key
"""""
    логирует в 2 журнала - общий и ошибки + выше, принимает __name__ и корень названия журнала
"""""


def set_logs(name, file_name) -> logging:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig\
        (level=logging.DEBUG,
         filename='.\\logs\\app_tmp.log',
         filemode='w',
         format=log_format,
         datefmt='%d-%b-%y %H:%M:%S')
    logger = logging.getLogger(name)

    c_format = \
        logging.Formatter(fmt=log_format, datefmt='%d-%m-%y %H:%M:%S')
    # log - debug level and higher
    debug_log = logging.FileHandler('.\\logs\\' + file_name + '.log')
    # log errors
    error_log = logging.FileHandler('.\\logs\\' + file_name + 'Error.log')
    if get_key('my_env.env', 'APP_PRODUCTION') == 'True':
        debug_log.setLevel(logging.ERROR)
        error_log.setLevel(logging.CRITICAL)
    else:
        debug_log.setLevel(logging.DEBUG)
        error_log.setLevel(logging.ERROR)
    debug_log.setFormatter(c_format)
    error_log.setFormatter(c_format)
    logger.addHandler(error_log)
    logger.addHandler(debug_log)

    return logger
