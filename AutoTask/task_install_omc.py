#-*- coding: utf-8 -*-

import configparser
import logging.handlers
import os

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
    logger.info('AUTO TASK - OpenManager Client Install')
    logger.info('=======================================')

    config = configparser.ConfigParser()
    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')

