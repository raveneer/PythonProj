#-*- coding: utf-8 -*-

import configparser
import logging.handlers
import os
import FileEventHandler
import time
from slackclient import SlackClient

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logdir = '{0}\\log'.format(os.getcwd())

if not os.path.exists(logdir):
    os.makedirs(logdir)

logger = logging.getLogger('auto_task_log')
fileHandler = logging.FileHandler('{0}/autotask.log'.format(logdir))
streamHandler = logging.StreamHandler()

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    logger.info('=======================================')
    logger.info('AUTO TASK - File watch')
    logger.info('=======================================')

    config = configparser.ConfigParser()
    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')

    #슬랙
    slack_client = SlackClient(config.get('slack', 'bot_token'))

    # 이벤트 핸들러를 생성하고, 초기화
    event_handler = FileEventHandler.FileEventHandler(slack_client)
    event_handler.set_param(config.get('monitoring', 'filter_key').split('|'), config.get('slack', 'channel'))

    # 모니터링 클래스 생성하고, 이벤트 핸들러를 붙여서 감시 시작
    observer = Observer()
    observer.schedule(event_handler, path=config.get('monitoring', 'log_dir'), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
            config.read('.\config.txt')
            event_handler.set_param(config.get('monitoring', 'filter_key').split('|'), config.get('slack', 'channel'))
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

