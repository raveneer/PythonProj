#-*- coding: utf-8 -*-

import time
import subprocess


class Installer(object):

    shieldPath = 'C:\\Program Files (x86)\\InstallShield\\2010\\System\\ISCmdBld.exe'

    def __init__(self, ismfileList, version):
        now = time.localtime()
        cur_time = "%02d%02d.%02d" % (now.tm_year % 1000, now.tm_mon, now.tm_mday)
        self.new_version = '{0}.{1}'.format(version, cur_time)
        self.ismfileList = ismfileList[:]
        return

    def versioninfoUpdate(self):

        for file_path in self.ismfileList:
            ism_file = open(file_path, "r+", encoding="utf-8")
            while True:
                pre_pos = ism_file.tell()
                line = ism_file.readline()
                if (line):
                    if line.find("ProductVersion") > 0:
                        line = "\t\t<row><td>ProductVersion</td><td>" + self.new_version + "</td><td/></row>\n"
                        ism_file.seek(pre_pos)
                        ism_file.write(line)
                        break
                else:
                    break

            ism_file.close()
        return

    def buildISM(self, buildArgs):
        for argList in buildArgs:
            subprocess.call([self.shieldPath, '-p', '{0}\\{1}'.format( argList[0], argList[1]), '-r', argList[2], '-c','COMP', '-a', 'Media'])
        return

    def buildISM(self, buildArgs):
        for argList in buildArgs:
            subprocess.call([self.shieldPath, '-p', '{0}\\{1}'.format( argList[0], argList[1]), '-r', argList[2], '-c COMP -a', 'Media'])
        return

