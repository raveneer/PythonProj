#-*- coding: utf-8 -*-

import configparser
import logging.handlers
import os
import random

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
    logger.info('AUTO TASK - Lotto645 Create')


    config = configparser.ConfigParser()
    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')

    #중복되지 않는 30개의 숫자를 뽑아서 랜덤한 숫자로 섞은 다음 5개의 게임을 만들어 텍스트로 저장한다
    lotto_numbers = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1]
    lotto_games = []
    lotto_single = []

    while len(lotto_games) !=5 :

        random_number = random.randrange(1, 45)
        if lotto_numbers[random_number] == 1 :
            lotto_numbers[random_number] = 0
            lotto_single.append(random_number)

        if len(lotto_single) == 6 :
            lotto_single.sort()
            lotto_games.append(lotto_single)
            lotto_single = []

    for lotto in lotto_games:
        print (lotto)

