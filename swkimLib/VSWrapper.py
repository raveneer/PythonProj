#-*- coding: utf-8 -*-

import subprocess
import enum

class VisualStudionVerionEnum(enum.Enum):
    VS6 = 1
    VS2008 = 2



class VisualStudio(object):

    #일단 기본값은 VS6에 맞춘다.
    visualStudio = VisualStudionVerionEnum.VS6
    compilePath = 'C:\\Program Files (x86)\\Microsoft Visual Studio\\Common\\MSDev98\\Bin\\msdev.exe'

    def __init__(self, vsVersion):
        print("Visual Studio  init")
        if vsVersion == VisualStudionVerionEnum.VS2008:
            self.compilePath = 'C:\\WINDOWS\\Microsoft.NET\\Framework\\v3.5\\MSBuild.exe'
            self.visualStudio = vsVersion


    def CleanProject(self, paramList = {}):
        print("Visual Studio  Clean")
        if self.visualStudio == VisualStudionVerionEnum.VS6:
            keyList = paramList.keys()
            for key in keyList:
                proc = subprocess.Popen([self.compilePath, paramList[key], '/MAKE', key,  '/CLEAN'], stdout=subprocess.PIPE)
                proc.communicate()

    def BuildProject(self, paramList={}):
        print("Visual Studio  Build")
        if self.visualStudio == VisualStudionVerionEnum.VS6:
            keyList = paramList.keys()
            for key in keyList:
                proc = subprocess.Popen([self.compilePath, paramList[key], '/MAKE', key], stdout=subprocess.PIPE)
                proc.communicate()