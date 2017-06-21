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
            keyList = paramList.keys()
            for key in keyList:
                result = subprocess.run([self.compilePath, paramList[key], '/MAKE', key, '/CLEAN'], stdout=subprocess.PIPE)
                self.mylogger.info('PROJECT CLEAN\n{0}'.format(result.stdout.decode('utf-8')))


    def BuildProject(self, projectList=[]):
        #빌드 로그는 커서 다른 파일에 저장한다.
        stdlog = open('{0}\\build_{1}.log'.format(self.buildlogdir, self.curTume), 'a')
        self.mylogger.info('PROJECT BUILD START')
        if self.visualStudio == VisualStudionVerionEnum.VS6:
            for projectArgList in projectList:
                args = [self.compilePath, projectArgList[0], '/MAKE', projectArgList[1]]
                subprocess.run(args, stdout=stdlog)
        else :
            for projectArgList in projectList:
                args = [self.compilePath, projectArgList[0]] + projectArgList[1].split(" ")
                subprocess.run(args, stdout=stdlog)

        stdlog.close()
        self.mylogger.info('PROJECT BUILD END')