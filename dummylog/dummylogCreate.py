#-*- coding: utf-8 -*-

import logging.handlers
import os
import time

logdir = '{0}\\log'.format(os.getcwd())

if not os.path.exists(logdir):
    os.makedirs(logdir)

logger = logging.getLogger('auto_task_log')
fileHandler = logging.FileHandler('{0}/autotask.log'.format(logdir))
streamHandler = logging.StreamHandler()

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

work_root = os.getcwd()
dummy_log_content = '{0}/content.txt'.format(work_root)
dummy_log_path = '{0}/test.log'.format(work_root)

if __name__ == "__main__":
    logger.info('=======================================')
    logger.info('AUTO TASK - dummy write log')
    logger.info('=======================================')

    while True:
        now = time.localtime()
        dummy_log_path = '{0}/test_{1}{2:02d}{3:2d}{4:2d}.log'.format(work_root, now.tm_year, now.tm_mon , now.tm_mday, now.tm_hour)
        content_file = open(dummy_log_content, 'r')
        dummy_log_file = open(dummy_log_path, 'a')
        time.sleep(1)
        while True:
            line = content_file.readline()
            if not line: break
            dummy_log_file.write(line)
        content_file.close()
        dummy_log_file.close()

    logger.info('=======================================')
    logger.info('AUTO TASK - Finish')
    logger.info('=======================================')






