#-*- coding: utf-8 -*-

import os
import time
from slackclient import SlackClient
import botcommand
import logging

logging.basicConfig(filename='./slack.log',level=logging.DEBUG)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose

    #슬랙 클라이언트 생성
    slack_client = SlackClient('xoxb-176677785552-DV8Vnh65JADgen7XGNLf4BJV')


if slack_client.rtm_connect():
    print("아이엔소프트 슬랙봇이 시작되었습니다.")
    while True:
        command, channel = botcommand.parse_slack_output(slack_client.rtm_read())

        if command and channel:
            botcommand.handle_command(slack_client, command, channel)


        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print("슬랙봇 연결을 실패하였습니다. 봇아이디를 확인하세요.")

print("슬랙봇이 종료되었습니다.")