#-*- coding: utf-8 -*-

import configparser
import logging.handlers
import os
import subprocess


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
    logger.info('AUTO TASK - SVN UPDATE')
    logger.info('=======================================')

    config = configparser.ConfigParser()

    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')

    svnclientpath = 'svn'

    repositoryList = config.get('svn_update', 'repository').split('|')    

    if len(repositoryList) > 0:
        for repositoryToken in repositoryList:
            repository = repositoryToken.strip()
            logger.info('SVN CleanUp And UPDATE : [{0}]'.format(repository))
            subprocess.run([svnclientpath, 'cleanup', repository])
            subprocess.run([svnclientpath, 'update', repository])

    logger.info('=======================================')
    logger.info('SVN UPDATE END')
    logger.info('=======================================')
