#-*- coding: utf-8 -*-
from swkimLib import SVNClientWrapper
from swkimLib import VSWrapper
from swkimLib import BasicFunctions
import shutil
import os

# 로컬에서 저장된 svn의 경로
svnRepositoryList = ['D:\\NGF_FULL\\trunk\\OpenManager3.2x', 'D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer']

#vs6환경에서 clean하기 위한 프로젝트 파일명과 빌드 옵션을 map으로 만들어 준다.
OMCBuildProject = { 'OpenManager - Win32 R_Auth':'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Workspaces\\MainFullVersion\\MainFullVersion.dsw'
                    , 'About - Win32 Release':'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Workspaces\\ModulesCommon\\ModulesCommon.dsw'
                    , 'OMUpdater - Win32 Release':'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Workspaces\\Updater\\OMUpdater.dsw'}

MeshBuildProject = {'OpenManager - Win32 R_Auth_Mesh':'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Workspaces\\MainFullVersion\\MainFullVersion.dsw'
                    , 'OMUpdater - Win32 Release':'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Workspaces\\Updater\\MeshUpdater.dsw'}

IOMCBuildProject = {'OMUpdater - Win32 Release_IOMC':'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Workspaces\\Updater\\OMUpdater.dsw'}


#icon 복사 root
resRoot = 'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\MainApplication\\FullVersion\\res'

if __name__ == "__main__":
    print("NGF Client Auto Build Start")

    basicfunction = BasicFunctions()

    curTime = basicfunction.getCurrentTiem()
    print (curTime)

    
    #SVN 정리
    svnclient = SVNClientWrapper.SVNClient( svnRepositoryList )
    svnclient.svnRevert();
    svnclient.svnUpdate();
    
    #vs6 project clean
    vsclient = VSWrapper.VisualStudio(VSWrapper.VisualStudionVerionEnum.VS6)
    vsclient.CleanProject(OMCBuildProject)
    vsclient.CleanProject(MeshBuildProject)
    vsclient.CleanProject(IOMCBuildProject)

    ####################################################
    #########일반 OMC 처리하기
    shutil.copyfile('{0}\\omc_main.ico'.format(resRoot), '{0}\\openmanager.ico'.format(resRoot))
    shutil.copyfile('{0}\\omc_NGF.ico'.format(resRoot), '{0}\\NGF.ico'.format(resRoot))
    vsclient.BuildProject(OMCBuildProject)

    targetPathList  = ['bin', 'modules']
    releasePath     = 'D:\\NGF_FULL\\trunk\\OpenManager3.2x\\OpenManager\\Release'
    installerPath   = 'D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer\\SetupFile\\Common'
    patchPath       = 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}\\patch\\NGFClient.Auth'.format(curTime)

    basicfunction.copyUpdateModules(targetPathList, releasePath, installerPath, patchPath)

    ####################################################
    #########  MESH 처리하기
    shutil.copyfile('{0}\\mesh_main.ico'.format(resRoot), '{0}\\openmanager.ico'.format(resRoot))
    shutil.copyfile('{0}\\mesh_NGF.ico'.format(resRoot), '{0}\\NGF.ico'.format(resRoot))
    vsclient.BuildProject(MeshBuildProject)

    installerPath = 'D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer\\CustomSetupFile\\MESH'
    patchPath = 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}\\patch\\MESH'.format(curTime)

    basicfunction.copyUpdateModules(targetPathList, releasePath, installerPath, patchPath)

    ####################################################
    #########  MESH 처리하기
    vsclient.BuildProject(IOMCBuildProject)
    installerPath = 'D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer\\CustomSetupFile\\IOMC\\common'
    patchPath = 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}\\patch\\IOMC'.format(curTime)

    basicfunction.copyUpdateModules(targetPathList, releasePath, installerPath, patchPath)


    #install shield porductversion update

    #svn export

    #installer build

    #ftp upload

    #git backup

    #slack noti


    #end Main
    print("NGF Client Auto Build END")