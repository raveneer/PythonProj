#-*- coding: utf-8 -*-

from slacker import Slacker
import sys
import subprocess

#사전에 정의해야 하는 값들 정리
trac_url = "http://220.76.205.150:9999/trac/ticket/"
channel_name = "#Chappie"
#
bot_token = 'xoxb-176677785552-DV8Vnh65JADgen7XGNLf4BJV'
commit_dict = {
    'swkim':'김상우 과장',
    'jgkim':'김종균 차장',
    'dongan':'고승규 부장',
    'nmpark':'박나미 대리',
	'nhkim':'김남호 과장'
               }
#svn repo path로 제품이름을 찾으니까 그냥 풀패스를 넣어주자
product_dict = {
    'unknown':'알수없는제품',
    'D:\svn_trac\svn\svn_repo\PerformanceView':'WaperClient',
    'D:\svn_trac\svn\svn_repo\OpenManager3':'NGF Server',
	'D:\svn_trac\svn\svn_repo\OMW2.0':'OMW',
	'D:\svn_trac\svn\svn_repo\CLIENT3':'NGF Client'
                }

#테스트를 위해서 값을 넣은것임..
svn_rev = "2997"
svn_path = "D:\svn_trac\svn\svn_repo\PerformanceView"

if len(sys.argv) > 2 :
   svn_rev = sys.argv[1]
   svn_path = sys.argv[2]
else :
    channel_name = "@kimsangwoo"
#end if

PIPE = subprocess.PIPE

#svnlook을 통해서 log를 얻는다.윈도우 기본 캐릭터 셋이 cp949 라서 한글이 깨진다.
cmd_svn_log = "svnlook log -r" + svn_rev + " " + svn_path
p = subprocess.Popen(cmd_svn_log, stdin=PIPE, stdout=PIPE)
svn_log = p.stdout.read().decode("cp949")

if svn_log=="" :
    svn_log ="test log  -#1313"

#svnlook을 통해서 작성자 이름을 얻는다. 작성자 이름은 영어니까 decode는 하지 않는다.
cmd_svn_author = "svnlook author -r "+ svn_rev + " " + svn_path
p = subprocess.Popen(cmd_svn_author, stdin=PIPE, stdout=PIPE)
svn_author = p.stdout.read()
svn_author = svn_author.strip()

if svn_author == "" :
    svn_author = "swkim"

# 커밋 로그에 '#1234' 형식이 있는 경우 트랙 번호로 생각해서 변환해 준다. 공백으로 토큰을 구분하니 반드시 한칸을 띄어야 한다.
trac_ticket_url = ""
log_list = svn_log.split()
for log_token in log_list :
    start_pos = log_token.find('#')
    if start_pos >= 0 :
        log_token = log_token[start_pos + 1: len(log_token) - start_pos + 1]
        trac_ticket_url = "{0}{1}".format(trac_url, log_token.replace('#', ""))
        break
    #end if
#end for



slack = Slacker(bot_token)

title_text = "{0}님이 {1}을 변경하였습니다.\n변경된 리비전은 {2}입니다.".format(commit_dict.get(svn_author, svn_author), product_dict.get(svn_path, svn_path), svn_rev)
pretext = "{0} 제품이 변경되었습니다.".format(product_dict.get(svn_path, svn_path))

attachments_dict = dict()
attachments_dict['pretext'] = pretext
attachments_dict['title'] = title_text
attachments_dict['fallback'] = pretext
attachments_dict['text'] = svn_log
attachments_dict['mrkdwn_in'] = ["text", "pretext"]


if trac_ticket_url != "" :
    new_pretext = "{0}\nTRAC : {1}".format(pretext, trac_ticket_url)
    attachments_dict['pretext'] =  new_pretext

attachments = [attachments_dict]

slack.chat.post_message(channel_name, text=None, attachments=attachments, as_user=True)
