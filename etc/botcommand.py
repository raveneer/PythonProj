#-*- coding: utf-8 -*-
import commandExecute

'''
주로.. 커맨드를 파싱하고, 결과를 받아서 슬랙 채널에 뿌려준다
'''
AT_BOT = "<@U56KXP3G8>"

def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']

    return None, None


def handle_command(slack_client, command, channel):
    #command를 공백으로 구분해서 목록을 만들어 보자.
    command_list = command.split()
    for command_token in command_list:
        if command_token == '미세먼지' :
            #미세먼지 정보 알려주기
            attachments = commandExecute.execute_air_info()
            break

        if command_token == 'ngf빌드' :
            #NGF 빌드 하기
            attachments = commandExecute.execute_auto_build(slack_client, channel, 'ngf')
            break

        if command_token == 'dof빌드' :
            #DOF 빌드 하기
            attachments = commandExecute.execute_auto_build(slack_client, channel,'dof')
            break
    # end for

    slack_client.api_call("chat.postMessage", channel=channel, text=None, attachments=attachments, as_user=True)

