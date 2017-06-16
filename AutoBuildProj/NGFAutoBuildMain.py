#-*- coding: utf-8 -*-
from swkimLib import SVNClientWrapper
from swkimLib import VSWrapper
from swkimLib import BasicFunctions
from swkimLib import InstallerWrapper
import shutil
import subprocess
import os
from slackclient import SlackClient

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
    curTime = basicfunction.getCurrentTime()



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

    ismList = []
    ismList.append("D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer\\OpenManager 3.2.ism")
    ismList.append("D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer\\CloudMesh_Lite.ism")
    ismList.append("D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer\\OpenManager 3.2_IOMC.ism")
    installshield = InstallerWrapper.Installer(ismList, '3.4')
    installshield.versioninfoUpdate()

    #svn export
    svnclient.svnExport('D:\\NGF_FULL\\trunk\\OpenManager 3.2 Installer', 'D:\\NGF_FULL\\trunk\\autobuild\\{0}'.format(curTime))



    #installer build
    del ismList[:]

    workdir = 'D:\\NGF_FULL\\trunk\\autobuild\\{0}'.format(curTime)
    omc_arg = [workdir, 'OpenManager 3.2.ism', 'Release_AUTHORITY']
    mesh_arg = [workdir, 'CloudMesh_Lite.ism', 'Release_Mesh_Authority']
    iomc_arg = [workdir, 'OpenManager 3.2_IOMC.ism', 'IOMC_Auth']

    ismList.append(omc_arg)
    ismList.append(mesh_arg)
    ismList.append(iomc_arg)
    installshield.buildISM(ismList)


    if not os.path.exists( 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}'.format(curTime) ):
        os.makedirs( 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}'.format(curTime) )

    shutil.copyfile('{0}\\ReleaseInstaller\\OMCAuthority_3.4.exe'.format(workdir), 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}\\OMCAuthority_3.4.{0}.exe'.format(curTime))
    shutil.copyfile('{0}\\ReleaseInstaller\\CloudMeshAuthority_3.4.exe'.format(workdir), 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}\\CloudMeshAuthority_3.4.{0}.exe'.format(curTime))
    shutil.copyfile('{0}\\ReleaseInstaller\\IOMC_3.4.exe'.format(workdir), 'D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}\\IOMC_3.4.{0}.exe'.format(curTime))

    print ( 'ftp upload start')

    #win scp ftp upload
    subprocess.call(['C:\\Program Files (x86)\\WinSCP\\WinSCP.exe'
                     , '/command'
                     , 'option batch abort'
                     , 'option confirm off'
                     , 'option transfer binary'
                     , 'open ftp://ubicom:ubicom!23@220.76.205.150:10021/OpenManager3/release/client/autobuild'
                     , 'put D:\\Upload\\OpenManager3\\release\\autobuild\\3.4.{0}'.format(curTime)
                     , 'close'
                     , 'exit'
                     ])
    print ('ftp upload END')


    #git backup
    print ('GIT Backup')
    subprocess.call([ "c:\\Program Files (x86)\\Git\\bin\\git.exe"
                      , '-C'
                      , "D:\\svn_backup\\NGF"
                      , 'svn'
                      , 'fetch'
                      ])
    #slack noti
    print ('Slack notify')
    slack_client = SlackClient('')
    slack_client.api_call("chat.postMessage", channel='#Chappie', text='NGF Build 완료', as_user=True)


    #end Main
    print("NGF Client Auto Build END")