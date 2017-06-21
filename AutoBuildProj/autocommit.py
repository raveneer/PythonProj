# -*- coding: utf-8 -*-

import sys
import os
import configparser
from Lib import SVNClientWrapper

if __name__ == "__main__":
    project = 'empty'
    config = configparser.ConfigParser()

    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')

    if 2 == len(sys.argv):
        project = sys.argv[1]

    #Auto Build Commit 을 로그로 남기면서 빌드된 인스톨러 형상을 저장한다.
    project_trunk = config.get(project, 'proj_root')
    svnclient = SVNClientWrapper.SVNClient([project_trunk])
    svnclient.svnCommit('Auto Build Commit')

    #svn에서 최신 로그 부터 이전 Auto Build Commit 로그까지 커밋 내용을 덤프 한다.


