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
    logger.info('OMAGENT Module AutoBuild Start')
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
    agent_module_source = '{0}\\nt\\modules\\windows'.format(agent_proj_trunk)
    agent_module_project = '{0}\\nt\\modules\\projs'.format(agent_proj_trunk)
    agent_release_x86_root = '{0}\\nt\\Win32\\Release'.format(agent_proj_trunk)
    agent_release_x64_root = '{0}\\nt\\x64\\Release'.format(agent_proj_trunk)
    agent_installer_root = '{0}\\nt\\InstallShield'.format(agent_proj_trunk)

    #빌드 현재 시간을 얻는다.
    basicfunction = BasicFunctions.BasicFunctions()
    curTime = basicfunction.getCurrentTime()
    
    #로컬에 저장된 svn 경로를 저장하고, revert 및 업데이트를 한다.
    svnRepositoryList = [agent_module_source, agent_module_project]
    svnclient = SVNClientWrapper.SVNClient(svnRepositoryList)

    svnclient.svnRevert();
    svnclient.svnUpdate();



    #vs2008 객체 생성
    vsclient = VSWrapper.VisualStudio(VSWrapper.VisualStudionVerionEnum.VS2008, logdir, curTime)

    ####################################################
    ######### 인스톨러로 배포되는 32/64bit 및 모든 빌드를 한번에 한다.
    OMAgentFullBuild = [
        ['{0}\\nt\\modules\\modules.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release']
        , ['{0}\\nt\\modules\\modules.sln'.format(agent_proj_trunk), '/t:Rebuild /p:Configuration=Release /p:Platform=x64']
    ]

    vsclient.BuildProject(OMAgentFullBuild)

    targetPathList = ['modules']

    x86patchPath = '{0}\\patch\\AgentNT_x86'.format(agent_autobuild)
    x86installerPath = '{0}\\modules\\x86_release'.format(agent_installer_root)
    basicfunction.copyUpdateModules(targetPathList, agent_release_x86_root, x86installerPath, x86patchPath)

    x64patchPath = '{0}\\patch\\AgentNT_x64'.format(agent_autobuild)
    x64installerPath = '{0}\\modules\\x64_release'.format(agent_installer_root)
    basicfunction.copyUpdateModules(targetPathList, agent_release_x64_root, x64installerPath, x64patchPath)

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