# -*- coding: utf-8 -*-

from slackclient import SlackClient
from Lib import insoftbot
import configparser
import time

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('.\config.txt')

    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose

    # 슬랙 클라이언트 생성
    slack_client = SlackClient( config.get('slack', 'bot_token') )
    mybot = insoftbot.INsoftBot()
    mybot.set_bot_id(slack_client, 'chappiebot')
    mybot.set_autobuild_root(config.get('slack', 'auto_build'))

if slack_client.rtm_connect():
    while True:
        command, channel = mybot.parse_slack_output(slack_client.rtm_read())

        if command and channel:
            mybot.handle_command(slack_client, command, channel)

        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print("슬랙봇 연결을 실패하였습니다. 봇아이디를 확인하세요.")

print("슬랙봇이 종료되었습니다.")
