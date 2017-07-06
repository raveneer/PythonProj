# -*- coding: utf-8 -*-
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

# 로그를 남길 폴더를 만들고, 스트림 핸들러와 파일 핸들러를 붙여준다.
logdir = '{0}\\log'.format(os.getcwd())

if not os.path.exists(logdir):
    os.makedirs(logdir)

logger = logging.getLogger('auto_build_logger')
fileHandler = logging.FileHandler('{0}/autobuild_dof_{1}.log'.format(logdir, curTime))
streamHandler = logging.StreamHandler()

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":

    logger.info('=======================================')
    logger.info('DOF Client AutoBuild Start')
    logger.info('=======================================')


    # 같은 경로에 있는 config.txt 파일을 읽어서 기본 root의 정보를 얻는다.
    config = configparser.ConfigParser()

    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')
        config.set('DOF', 'autobuild', '{0}\\5.0.{1}'.format(config.get('DOF', 'autobuild'), curTime))


    dof_proj_trunk = config.get('DOF', 'proj_root')
    dof_autobuild = config.get('DOF', 'autobuild')
    ftp_upload = config.get('DOF', 'ftp_upload')

    # trunk에서 시작하는 경로는 변경 될 수 없다.
    dof_installer_root = '{0}\\OpenManager 5.0 Installer'.format(dof_proj_trunk)
    dof_source_root = '{0}\\OpenManager_DOF'.format(dof_proj_trunk)
    dof_workspaces_path = '{0}\\OpenManager\\Workspaces'.format(dof_source_root)
    dof_release_root = '{0}\\OpenManager\\Release'.format(dof_source_root)

    # 로컬에서 저장된 svn의 경로


    # vs2008 환경에서 빌드 하기 위한 프로젝트 파일명과 빌드 옵션을 map으로 만들어 준다.
    OMCBuildProject = [
          ['{0}\\MainFullVersion\\MainFullVersion.sln'.format(dof_workspaces_path), '/t:Rebuild /p:Configuration=Release']
        , ['{0}\\ModulesCommon\\ModulesCommon.sln'.format(dof_workspaces_path), '/t:Rebuild /p:Configuration=Release']
    ]

    AnycatcherBuildProject = [
        '{0}\\MainFullVersion\\AnyCatcher.sln'.format(dof_workspaces_path), '/t:Rebuild /p:Configuration=Release_AnyCatcher'
    ]

    BTVBuildProject = [
        '{0}\\OpenManager\\Modules\\Custom\\BTV\\BTV_full.sln'.format(dof_source_root), '/t:Rebuild /p:Configuration=Release_BTV'
    ]

    # 빌드 현재 시간을 얻는다.
    basicfunction = BasicFunctions.BasicFunctions()
    curTime = basicfunction.getCurrentTime()

    # 로컬에 저장된 svn 경로를 저장하고, revert 및 업데이트를 한다.
    svnRepositoryList = [dof_source_root, dof_installer_root]
    svnclient = SVNClientWrapper.SVNClient(svnRepositoryList)

    svnclient.svnRevert();
    svnclient.svnUpdate();

    #vs2008 객체 생성
    vsclient = VSWrapper.VisualStudio(VSWrapper.VisualStudionVerionEnum.VS2008, logdir, curTime)

    ####################################################
    #########일반 OMC 처리하기

    #vsclient.BuildProject(OMCBuildProject)

    targetPathList = ['bin', 'modules']

    installerPath = '{0}\\SetupFile\\Common'.format(dof_installer_root)
    patchPath = '{0}\\patch\\DOFClient'.format(dof_autobuild)

    basicfunction.copyUpdateModules(targetPathList, dof_release_root, installerPath, patchPath)

    ####################################################
    #########  anycatcher 처리하기
    #vsclient.BuildProject(AnycatcherBuildProject)

    installerPath = '{0}\\CustomSetupFile\\AnyCatcher\\Common'.format(dof_installer_root)
    patchPath = '{0}\\patch\\AnycatcherClient'.format(dof_autobuild)

    basicfunction.copyUpdateModules(targetPathList, dof_release_root + 'Anycatcher', installerPath, patchPath)

    ####################################################
    #########  BTV 처리하기
    #vsclient.BuildProject(BTVBuildProject)

    installerPath = '{0}\\CustomSetupFile\\BTV\\Common'.format(dof_installer_root)
    patchPath = '{0}\\patch\\BTVClient'.format(dof_autobuild)

    basicfunction.copyUpdateModules(targetPathList, dof_release_root + 'Btv', installerPath, patchPath)

    # install shield porductversion update

    ismList = []
    ismList.append("{0}\\AnyCatcher.ism".format(dof_installer_root))
    ismList.append("{0}\\OpenManager 5.0_Lite.ism".format(dof_installer_root))
    installshield = InstallerWrapper.Installer( '5.0')
    installshield.versioninfoUpdate(ismList)

    # svn export
    export_path = '{0}\\autobuild\\{1}'.format(dof_proj_trunk, curTime)
    if not os.path.exists(export_path):
        os.makedirs(export_path)
        
    svnclient.svnExport(dof_installer_root, export_path)

    # installer build
    workdir = '{0}\\autobuild\\{1}'.format(dof_proj_trunk, curTime)

    del ismList[:]
    omc_arg = [workdir, 'OpenManager 5.0_Lite.ism', 'Release_Common']
    any_arg = [workdir, 'OpenManager 5.0_Lite.ism', 'Release_BTV']
    btv_arg = [workdir, 'AnyCatcher.ism', 'Release_AnyCatcher']

    ismList.append(['-p', '{0}\\OpenManager 5.0_Lite.ism'.format(workdir),      '-r', 'Release_Common',         '-c', 'COMP', '-a', 'Media'])
    ismList.append(['-p', '{0}\\OpenManager 5.0_Lite.ism'.format(workdir),      '-r', 'Release_BTV',            '-c', 'COMP', '-a', 'Media'])
    ismList.append(['-p', '{0}\\AnyCatcher.ism'.format(workdir),                  '-r', 'Release_AnyCatcher',   '-c', 'COMP', '-a', 'Media'])
    installshield.buildISM(ismList)

    if not os.path.exists(dof_autobuild):
        os.makedirs(dof_autobuild)

    shutil.copyfile('{0}\\ReleaseInstaller\\AnyCatcher3.0_5.0.exe'.format(workdir),
                    '{0}\\AnyCatcher3.0_5.0.{1}.exe'.format(dof_autobuild, curTime))
    shutil.copyfile('{0}\\ReleaseInstaller\\OMC_5.0.exe'.format(workdir),
                    '{0}\\OMC_5.0.{1}.exe'.format(dof_autobuild, curTime))
    shutil.copyfile('{0}\\ReleaseInstaller\\OMCBtv_5.0.exe'.format(workdir),
                    '{0}\\OMCBtv_5.0.{1}.exe'.format(dof_autobuild, curTime))

    svnclient.dumpCommitlog(dof_proj_trunk, '{0}/autobuild_dof_commit_dump{1}.txt'.format(logdir, curTime))
    logger.info('ftp upload start')

    # win scp ftp upload
    subprocess.call(['C:\\Program Files (x86)\\WinSCP\\WinSCP.exe'
                        , '/command'
                        , 'option batch abort'
                        , 'option confirm off'
                        , 'option transfer binary'
                        , 'open ftp://{0}'.format(ftp_upload)
                        , 'put {0}'.format(dof_autobuild)
                        , 'close'
                        , 'exit'
                     ])
    logger.info('ftp upload END')

    # git backup
    logger.info('GIT Backup')
    subprocess.call(["c:\\Program Files (x86)\\Git\\bin\\git.exe"
                        , '-C'
                        , "D:\\svn_backup\\DOF"
                        , 'svn'
                        , 'fetch'
                     ])

    # 배포 사이트 주소
    ftp_ip = ftp_upload[ftp_upload.find('@') + 1:ftp_upload.rfind(':')]
    ftp_path = ftp_upload[ftp_upload.find('/'):]
    ftp_url = 'http://{0}:10003{1}/5.0.{2}'.format(ftp_ip, ftp_path, curTime)

    # slack noti
    logger.info('Slack notify')
    slack_client = SlackClient(config.get('slack', 'bot_token'))
    slack_client.api_call("chat.postMessage", channel=config.get('slack', 'channel'), text='DOF Build 완료\n{0}'.format(ftp_url), as_user=True)

    # end Main
    logger.info("NGF Client Auto Build END")