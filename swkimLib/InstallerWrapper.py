#-*- coding: utf-8 -*-

import time

class Installer(object):
    def __init__(self):
        now = time.localtime()
        self.dof_version = "5.0.%02d%02d.%02d" % (now.tm_year % 1000, now.tm_mon, now.tm_mday)
        self.ngf_version = "3.4.%02d%02d.%02d" % (now.tm_year % 1000, now.tm_mon, now.tm_mday)
        return

