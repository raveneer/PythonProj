#-*- coding: utf-8 -*-

import subprocess
import enum
import logging

class VisualStudionVerionEnum(enum.Enum):
    VS6 = 1
    VS2008 = 2



class VisualStudio(object):

    #일단 기본값은 VS6에 맞춘다.
    visualStudio = VisualStudionVerionEnum.VS6
    compilePath = 'C:\\Program Files (x86)\\Microsoft Visual Studio\\Common\\MSDev98\\Bin\\msdev.exe'

    def __init__(self, vsVersion, logdir, curTime):
        self.mylogger = logging.getLogger('auto_build_logger')
        self.buildlogdir = logdir
        self.curTume = curTime
        if vsVersion == VisualStudionVerionEnum.VS2008:
            self.compilePath = 'C:\\WINDOWS\\Microsoft.NET\\Framework\\v3.5\\MSBuild.exe'
            self.visualStudio = vsVersion
            self.mylogger.info('Visual studio 2008')
        else:
            self.mylogger.info('Visual studio 6.0')


    def CleanProject(self, paramList = {}):
        if self.visualStudio == VisualStudionVerionEnum.VS6:
            self.mylogger.info('VS6 Project Clean - START')
            projectfile_list = []
            for project in paramList:
                subprocess.run([self.compilePath, project[0], '/MAKE', project[1], '/CLEAN'], stdout=subprocess.PIPE)
                projectfile_list.append(project[0])
            self.mylogger.info(projectfile_list)
            self.mylogger.info('VS6 Project Clean - END')


    def BuildProject(self, projectList=[]):
        logfile = open('buildlog.log', 'a')

        self.mylogger.info('PROJECT BUILD START')
        if self.visualStudio == VisualStudionVerionEnum.VS6:
            for projectArgList in projectList:
                args = [self.compilePath, projectArgList[0], '/MAKE', projectArgList[1]]
                subprocess.run(args)
        else :
            for projectArgList in projectList:
                args = [self.compilePath, projectArgList[0]] + projectArgList[1].split(" ")
                subprocess.run(args, stdout=logfile)
        self.mylogger.info('PROJECT BUILD END')
        logfile.close