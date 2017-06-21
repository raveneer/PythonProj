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
fileHandler = logging.FileHandler('{0}/autobuild_agent_{1}.log'.format(logdir, curTime))
streamHandler = logging.StreamHandler()

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":

    logger.info('=======================================')
    logger.info('OMAGENT Client AutoBuild Start')
    logger.info('=======================================')

    # 같은 경로에 있는 config.txt 파일을 읽어서 기본 root의 정보를 얻는다.
    config = configparser.ConfigParser()

    if os.path.exists('.\config.txt'):
        config.read('.\config.txt')
        config.set('AGENT', 'autobuild', '{0}\\3.0.{1}'.format(config.get('AGENT', 'autobuild'), curTime))

    agent_proj_trunk = config.get('AGENT', 'proj_root')
    agent_autobuild = config.get('AGENT', 'autobuild')
    ftp_upload = config.get('AGENT', 'ftp_upload')

    # trunk에서 시작하는 경로는 변경 될 수 없다.
    agent_installer_root = '{0}\\nt\\InstallShield'.format(agent_proj_trunk)
    agent_source_root = '{0}\\unix\\lib'.format(agent_proj_trunk)
    agent_module_root = '{0}\\nt\\modules\\windows'.format(agent_proj_trunk)
    agent_release_x86_root = '{0}\\nt\\Win32\\Release'.format(agent_proj_trunk)
    agent_release_x64_root = '{0}\\nt\\x64\\Release'.format(agent_proj_trunk)

    #빌드 현재 시간을 얻는다.
    basicfunction = BasicFunctions.BasicFunctions()
    curTime = basicfunction.getCurrentTime()
    
    #로컬에 저장된 svn 경로를 저장하고, revert 및 업데이트를 한다.
    svnRepositoryList = [agent_source_root, agent_installer_root, agent_module_root]
    svnclient = SVNClientWrapper.SVNClient(svnRepositoryList)

    svnclient.svnRevert();
    svnclient.svnUpdate();



    #vs2008 객체 생성
    vsclient = VSWrapper.VisualStudio(VSWrapper.VisualStudionVerionEnum.VS2008, logdir, curTime)

    ####################################################
    ######### 인스톨러로 배포되는 32/64bit 및 모든 빌드를 한번에 한다.
    OMAgentFullBuild = [
        ['{0}\\nt\\coreXYZ\\NGFAgentNT.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release']
        , ['{0}\\nt\\coreXYZ\\NGFAgentNT.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release_wAgent']
        , ['{0}\\nt\\WindowUI\\NGFAgent\\NGFAgent.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release']
        , ['{0}\\nt\\WindowUI\\NGFAgent\\NGFAgent.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release_Anycathcer']
        , ['{0}\\nt\\WindowUI\\NGFAgent\\NGFAgent.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release_Swdiscovery']
        , ['{0}\\nt\\coreXYZ\\NGFAgentNT.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release /p:Platform=x64']
        , ['{0}\\nt\\coreXYZ\\NGFAgentNT.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release_wAgent /p:Platform=x64']
        , ['{0}\\nt\\WindowUI\\NGFAgent\\NGFAgent.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release /p:Platform=x64']
        , ['{0}\\nt\\WindowUI\\NGFAgent\\NGFAgent.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release_Anycathcer /p:Platform=x64']
        , ['{0}\\nt\\WindowUI\\NGFAgent\\NGFAgent.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release_Swdiscovery /p:Platform=x64']
    ]

    vsclient.BuildProject(OMAgentFullBuild)

    targetPathList = ['core', 'bin_swad', 'bin_common', 'bin_anycatcher']

    x86Install = '{0}\\SetupFiles\\x86_release'.format(agent_installer_root)
    x86patchPath = '{0}\\patch\\AgentNT_x86'.format(agent_autobuild)
    basicfunction.copyUpdateModules(targetPathList, agent_release_x86_root, x86Install, x86patchPath)

    x64Install = '{0}\\SetupFiles\\x64_release'.format(agent_installer_root)
    x64patchPath = '{0}\\patch\\AgentNT_x86'.format(agent_autobuild)
    basicfunction.copyUpdateModules(targetPathList, agent_release_x64_root, x64Install, x64patchPath)



    # svn export
    export_path = '{0}\\autobuild\\{1}'.format(agent_proj_trunk, curTime)
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    svnclient.svnExport(agent_installer_root, export_path)

    # installer build

    workdir = '{0}\\autobuild\\{1}'.format(agent_proj_trunk, curTime)
    ismList = []
    ismList.append( ['-p', '{0}\\Any_Win2012_x64.ism'.format(workdir), '-r', 'SingleImage'] )
    ismList.append(['-p', '{0}\\Any_WinNT_x64.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\Any_WinNT_x86.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\NGFAgent_Win2012_x64.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\NGFAgent_WinNT_x64.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\NGFAgent_WinNT_x86.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\SWADAgent_Win2012_x64.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\SWADAgent_WinNT_x64.ism'.format(workdir), '-r', 'SingleImage'])
    ismList.append(['-p', '{0}\\SWADAgent_WinNT_x86.ism'.format(workdir), '-r', 'SingleImage'])
    installshield = InstallerWrapper.Installer('3.0')
    installshield.buildISM(ismList)


    if not os.path.exists(agent_autobuild):
        os.makedirs(agent_autobuild)

    shutil.copyfile('{0}\\installer\\x64\\Anycatcher\\setup.exe'.format(workdir),       '{0}\ACEMAgent.installer.win.intel.x64.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x64\\Anycatcher_2012\\setup.exe'.format(workdir),  '{0}\ACEMAgent2012.installer.win.intel.x64.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x64\\NGFAgent\\setup.exe'.format(workdir),         '{0}\OMAgent.installer.win.intel.x64.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x64\\NGFAgent_2012\\setup.exe'.format(workdir),    '{0}\OMAgent2012.installer.win.intel.x64.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x64\\swad\\setup.exe'.format(workdir),             '{0}\SWADAgent.installer.win.intel.x64.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x64\\swad_2012\\setup.exe'.format(workdir),        '{0}\SWADAgent2012.installer.win.intel.x64.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x86\\anycatcher\\setup.exe'.format(workdir),       '{0}\ACEMAgent.installer.win.intel.x86.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x86\\NGFAgent\\setup.exe'.format(workdir),         '{0}\OMAgent.installer.win.intel.x86.{1}.exe'.format(agent_autobuild, curTime))
    shutil.copyfile('{0}\\installer\\x86\\swad\\setup.exe'.format(workdir),             '{0}\SWADAgent.installer.win.intel.x86.{1}.exe'.format(agent_autobuild, curTime))

    svnclient.dumpCommitlog(agent_proj_trunk, '{0}/autobuild_agent_commit_dump{1}.txt'.format(logdir, curTime))


    logger.info('ftp upload start')

    # win scp ftp upload
    subprocess.call(['C:\\Program Files (x86)\\WinSCP\\WinSCP.exe'
                        , '/command'
                        , 'option batch abort'
                        , 'option confirm off'
                        , 'option transfer binary'
                        , 'open ftp://{0}'.format(ftp_upload)
                        , 'put {0}'.format(agent_autobuild)
                        , 'close'
                        , 'exit'
                     ])
    logger.info('ftp upload END')

    # git backup
    logger.info('GIT Backup')
    subprocess.call(["c:\\Program Files (x86)\\Git\\bin\\git.exe"
                        , '-C'
                        , "D:\\svn_backup\\OMAGENT"
                        , 'svn'
                        , 'fetch'
                     ])

    # 배포 사이트 주소
    ftp_ip = ftp_upload[ftp_upload.find('@') + 1:ftp_upload.rfind(':')]
    ftp_path = ftp_upload[ftp_upload.find('/'):]
    ftp_url = 'http://{0}:10003{1}/3.0.{2}'.format(ftp_ip, ftp_path, curTime)

    # slack noti
    logger.info('Slack notify')
    slack_client = SlackClient(config.get('slack', 'bot_token'))
    slack_client.api_call("chat.postMessage", channel=config.get('slack', 'channel'),
                          text='AGNET Build 완료\n{0}'.format(ftp_url), as_user=True)


    # end Main
    logger.info("AGNET Client Auto Build END")