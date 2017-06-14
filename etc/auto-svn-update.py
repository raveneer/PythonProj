#-*- coding: utf-8 -*-

import subprocess, os

#svn 경로를 리스트로 만들어 보자
svn_path_list = [ 'D:\Document'
                 ,'D:\DOF_FULL'
                 ,'D:\NGF_FULL'
                 ,'D:\OMAGENT'
                 ,'D:\PerformanceView']


#svn 실행 경로
svn_proc = 'C:\\Program Files\\TortoiseSVN\\bin\\svn.exe'

# svn경로를 하나씩 업데이트하는데 먼저 cleanup을 해주고, 업데이트를 해준다.
PIPE = subprocess.PIPE
for svn_repo in svn_path_list:
    #cleanup 부터..
    run_cmd = '{0} cleanup {1}'.format(svn_proc, svn_repo)
    p = subprocess.Popen(run_cmd, stdin=PIPE, stdout=PIPE)
    svn_log = p.stdout.read()
    os.system('taskkill.exe /f /im svn.exe')

    #실제 svn업데이트
    run_cmd = '{0} update {1}'.format(svn_proc, svn_repo)
    p = subprocess.Popen(run_cmd, stdin=PIPE, stdout=PIPE)
    svn_log = p.stdout.read()
    os.system('taskkill.exe /f /im svn.exe') #svn.exe를 죽여야 다음 업데이트가 동작한다.