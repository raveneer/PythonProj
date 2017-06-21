#-*- coding: utf-8 -*-
from Lib import SVNClientWrapper
from Lib import VSWrapper
from Lib import BasicFunctions
from Lib import InstallerWrapper

from slackclient import SlackClient

import shutil
import subprocess
import os
import logging.handlers
import configparser

basicfunction = BasicFunctions.BasicFunctions()
curTime = basicfunction.getCurrentTime()

#로그를 남길 폴더를 만들고, 스트림 핸들러와 파일 핸들러를 붙여준다.
logdir = '{0}\\log\\{1}'.format(os.getcwd(), curTime)

if not os.path.exists(logdir):
    os.makedirs(logdir)

logger          = logging.getLogger('auto_build_logger')
fileHandler     = logging.FileHandler('{0}/autobuild_ngf_{1}.log'.format(logdir, curTime))
streamHandler   = logging.StreamHandler()

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger.info('=======================================')
    logger.info('NGF Client AutoBuild Start')
    logger.info('=======================================')

    # 같은 경로에 있는 config.txt 파일을 읽어서 기본 root의 정보를 얻는다.
    config = configparser.ConfigParser()

    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')
        config.set('NGF', 'autobuild', '{0}\\3.4.{1}'.format(config.get('NGF', 'autobuild'), curTime))

    ngf_proj_trunk = config.get('NGF', 'proj_root')
    ngf_autobuild = config.get('NGF', 'autobuild')
    ftp_upload = config.get('NGF', 'ftp_upload')

    # trunk에서 시작하는 경로는 변경 될 수 없다.
    ngf_installer_root = '{0}\\OpenManager 3.2 Installer'.format(ngf_proj_trunk)
    ngf_source_root = '{0}\\OpenManager3.2x'.format(ngf_proj_trunk)
    ngf_workspaces_path = '{0}\\OpenManager\\Workspaces'.format(ngf_source_root)
    ngf_release_root = '{0}\\OpenManager\\Release'.format(ngf_source_root)




    # vs6환경에서 clean하기 위한 프로젝트 파일명과 빌드 옵션을 map으로 만들어 준다.
    OMCBuildProject = [
          ['{0}\\MainFullVersion\\MainFullVersion.dsw'.format(ngf_workspaces_path), 'OpenManager - Win32 R_Auth']
        , ['{0}\\ModulesCommon\\ModulesCommon.dsw'.format(ngf_workspaces_path), 'About - Win32 Release' ]
        , ['{0}\\Updater\\OMUpdater.dsw'.format(ngf_workspaces_path), 'OMUpdater - Win32 Release']
    ]

    MeshBuildProject = [
          ['{0}\\MainFullVersion\\MainFullVersion.dsw'.format(ngf_workspaces_path), 'OpenManager - Win32 R_Auth_Mesh']
        , ['{0}\\Updater\\MeshUpdater.dsw'.format(ngf_workspaces_path), 'OMUpdater - Win32 Release']

    ]

    IOMCBuildProject = [
        '{0}\\Updater\\OMUpdater.dsw'.format(ngf_workspaces_path), 'OMUpdater - Win32 Release_IOMC'
    ]


    # icon 복사 root
    resRoot = '{0}\\OpenManager\\MainApplication\\FullVersion\\res'.format(ngf_source_root)

    #빌드 시간을 얻는다.
    basicfunction = BasicFunctions.BasicFunctions()
    curTime = basicfunction.getCurrentTime()

    # 로컬에 저장된 svn 경로를 저장하고, revert 및 업데이트를 한다.
    svnRepositoryList = [ngf_source_root, ngf_installer_root]
    svnclient = SVNClientWrapper.SVNClient( svnRepositoryList )

    
    svnclient.svnRevert();
    svnclient.svnUpdate();
    
    #vs6 project clean
    vsclient = VSWrapper.VisualStudio(VSWrapper.VisualStudionVerionEnum.VS6, logdir, curTime)
    vsclient.CleanProject(OMCBuildProject)
    vsclient.CleanProject(MeshBuildProject)
    vsclient.CleanProject(IOMCBuildProject)

    ####################################################
    #########일반 OMC 처리하기
    shutil.copyfile('{0}\\omc_main.ico'.format(resRoot), '{0}\\openmanager.ico'.format(resRoot))
    shutil.copyfile('{0}\\omc_NGF.ico'.format(resRoot), '{0}\\NGF.ico'.format(resRoot))
    vsclient.BuildProject(OMCBuildProject)

    targetPathList  = ['bin', 'modules']

    installerPath   = '{0}\\SetupFile\\Common'.format(ngf_installer_root)
    patchPath       = '{0}\\patch\\NGFClient.Auth'.format(ngf_autobuild)

    basicfunction.copyUpdateModules(targetPathList, ngf_release_root, installerPath, patchPath)

    ####################################################
    #########  MESH 처리하기
    shutil.copyfile('{0}\\mesh_main.ico'.format(resRoot), '{0}\\openmanager.ico'.format(resRoot))
    shutil.copyfile('{0}\\mesh_NGF.ico'.format(resRoot), '{0}\\NGF.ico'.format(resRoot))
    vsclient.BuildProject(MeshBuildProject)

    installerPath = '{0}\\CustomSetupFile\\MESH'.format(ngf_installer_root)
    patchPath = '{0}\\patch\\MESH'.format(ngf_autobuild)

    basicfunction.copyUpdateModules(targetPathList, ngf_release_root, installerPath, patchPath)

    ####################################################
    #########  IOMC 처리하기
    vsclient.BuildProject(IOMCBuildProject)
    installerPath = '{0}\\CustomSetupFile\\IOMC\\common'.format(ngf_installer_root)
    patchPath = '{0}\\patch\\IOMC'.format(ngf_autobuild)

    basicfunction.copyUpdateModules(targetPathList, ngf_release_root, installerPath, patchPath)
    

    #install shield porductversion update

    ismList = []
    ismList.append("{0}\\OpenManager 3.2.ism".format(ngf_installer_root))
    ismList.append("{0}\\CloudMesh_Lite.ism".format(ngf_installer_root))
    ismList.append("{0}\\OpenManager 3.2_IOMC.ism".format(ngf_installer_root))
    installshield = InstallerWrapper.Installer('3.4')
    installshield.versioninfoUpdate(ismList)

    #svn export
    svnclient.svnExport(ngf_installer_root, '{0}\\autobuild\\{1}'.format(ngf_proj_trunk, curTime))



    #installer build

    workdir = '{0}\\autobuild\\{1}'.format(ngf_proj_trunk, curTime)
    omc_arg = [workdir, 'OpenManager 3.2.ism', 'Release_AUTHORITY']
    mesh_arg = [workdir, 'CloudMesh_Lite.ism', 'Release_Mesh_Authority']
    iomc_arg = [workdir, 'OpenManager 3.2_IOMC.ism', 'IOMC_Auth']

    ismList.append(omc_arg)
    ismList.append(mesh_arg)
    ismList.append(iomc_arg)
    installshield.buildISM(ismList)


    if not os.path.exists( ngf_autobuild ):
        os.makedirs( ngf_autobuild )

    shutil.copyfile('{0}\\ReleaseInstaller\\OMCAuthority_3.4.exe'.format(workdir), '{0}\\OMCAuthority_3.4.{1}.exe'.format(ngf_autobuild, curTime))
    shutil.copyfile('{0}\\ReleaseInstaller\\CloudMeshAuthority_3.4.exe'.format(workdir), '{0}\\CloudMeshAuthority_3.4.{1}.exe'.format(ngf_autobuild, curTime))
    shutil.copyfile('{0}\\ReleaseInstaller\\IOMC_3.4.exe'.format(workdir), '{0}\\IOMC_3.4.{1}.exe'.format(ngf_autobuild, curTime))

    logger.info('ftp upload start')

    #win scp ftp upload
    subprocess.call(['C:\\Program Files (x86)\\WinSCP\\WinSCP.exe'
                     , '/command'
                     , 'option batch abort'
                     , 'option confirm off'
                     , 'option transfer binary'
                     , 'open ftp://{0}'.format(ftp_upload)
                     , 'put {0}'.format(ngf_autobuild)
                     , 'close'
                     , 'exit'
                     ])
    logger.info('ftp upload END')


    #git backup
    logger.info ('GIT Backup')
    subprocess.call([ "c:\\Program Files (x86)\\Git\\bin\\git.exe"
                      , '-C'
                      , "D:\\svn_backup\\NGF"
                      , 'svn'
                      , 'fetch'
                      ])

    #배포 사이트 주소
    ftp_ip = ftp_upload[ftp_upload.find('@') + 1:ftp_upload.rfind(':')]
    ftp_path = ftp_upload[ftp_upload.find('/'):]
    ftp_url = 'http://{0}:10003{1}/3.4.{2}'.format(ftp_ip, ftp_path, curTime)

    #slack noti
    logger.info('Slack notify')
    slack_client = SlackClient(config.get('slack', 'bot_token'))
    slack_client.api_call("chat.postMessage", channel=config.get('slack', 'channel'), text='NGF Build 완료\n{0}'.format(ftp_url), as_user=True)


    #end Main
    logger.info("NGF Client Auto Build END")