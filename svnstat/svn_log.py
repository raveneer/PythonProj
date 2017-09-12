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


def LoadSVNLog(repository, map_month):
    open('svn_dump.txt', 'a').write('==========={0}===========\n'.format(repository))
    map_month.clear()
    proc = subprocess.Popen(['svn', 'log', repository, '-r', '{%s}:{%s}' % (start_date, end_date)], stdout=subprocess.PIPE)
    for byteline in proc.stdout.readlines():
        line = byteline.decode('cp949')
        if line != '\r\n':
            line = line.strip('\n')
            x = line.split('|')

            if len(x) != 4: continue

            rev = x[0].strip()[1:]
            user = x[1].strip()
            date = x[2].strip().split(' ')[0]
            year_month = date[:7]

            if not map_month.get(year_month):
                # {'year-month': {'user_name' : 0}}
                map_month[year_month] = {}

            map_user = map_month[year_month]
            if not map_user.get(user):
                map_user[user] = 0

            map_user[user] = map_user[user] + 1


    for key in map_month.keys() :
        open('svn_dump.txt', 'a').write(key + '\n')
        map_user = map_month[key]

        for userKey in map_user.keys() :
            open('svn_dump.txt', 'a').write('user : {0}, commit_count : {1}\n'.format(userKey, map_user[userKey]))


if __name__ == "__main__":
    logger.info('=======================================')
    logger.info('SVN Analyze')
    logger.info('=======================================')

    config = configparser.ConfigParser()
    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')

    start_date = config.get('svn_stat', 'start_date')
    end_date = config.get('svn_stat', 'end_date')
    svn_dump_path = config.get('svn_stat', 'dump_path')
    repositoryList = config.get('svn_stat', 'proj_root').split('|')

    if os.path.exists(svn_dump_path) :
        os.remove(svn_dump_path)

    #사용자별 정보를 저장하도록 한다.
    map_month = {}

    for repositoryToken in repositoryList:
        repository = repositoryToken.strip()
        LoadSVNLog(repository, map_month )


    #기간을 정해서 로그를 덤프 한다





    logger.info('=======================================')
    logger.info('Finish')
    logger.info('=======================================')

