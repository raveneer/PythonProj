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

    project_trunk = config.get(project, 'proj_root')
    svnclient = SVNClientWrapper.SVNClient([project_trunk])
    svnclient.svnCommit('Auto Build Commit')


