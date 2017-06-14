#-*- coding: utf-8 -*-
import os
import time
from slackclient import SlackClient
from airkoreaPy import AirKorea

BOT_ID = "U56KXP3G8"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
api_key = "jesIR41SPZnxR6T%2FeGyEfaj9KThVoglsiAvgOtBsZoH%2FYpNHmq%2BRi5kmRs0RmWHzhfAZphbOkBr5f75M%2FBpd%2Fg%3D%3D"
station_name = "서울"
# instantiate Slack & Twilio clients
slack_client = SlackClient('xoxb-176677785552-DV8Vnh65JADgen7XGNLf4BJV')


def handle_command(command, channel):

    response = "못알아 먹는 명령어입니다."

    '''만약 air 가 입력이 되는 경우'''
    if command == 'air' :
        airkorea = AirKorea(api_key)
        response = airkorea.forecast(station_name)
        attachments = make_air_quality_template(response)
        slack_client.api_call("chat.postMessage", channel=channel, text=None, attachments=attachments, as_user=True)
        time.sleep(READ_WEBSOCKET_DELAY)
    else :
        slack_client.api_call("chat.postMessage", channel=channel, text=command, as_user=True)




def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']

    return None, None


def AIR_QUALITY_COLOR(grade):
    grade = int(grade)
    if grade == 1:
        return "#1E90FF"
    elif grade == 2:
        return "#90EE90"
    elif grade == 3:
        return "#FF6347"
    else:
        return "#DC143C"


def AIR_QUALITY_TEXT(grade):
    grade = int(grade)
    if grade == 1:
        return "좋음"
    elif grade == 2:
        return "보통"
    elif grade == 3:
        return "나쁨"
    else:
        return "매우 나쁨"

def make_air_quality_template(data):
    attachments = []

    cai = data['cai']

    a_dict = {}
    a_dict['color'] = AIR_QUALITY_COLOR(cai['grade'])
    a_dict['fallback'] = cai['description'] + " : " + cai['value']
    a_dict['title'] = data['stationname'] + "의 대기질 정보 입니다."
    a_dict['mrkdwn_in'] = ["text", "pretext"]

    fields = []
    field = {
        "title": cai['description'],
        "value": cai['value'] + "점"
    }
    fields.append(field)
    del data['cai']
    del data['pm25']

    for k, v in data.items():
        if isinstance(v, str):
            continue
        field = {}

        field['title'] = v['description']
        field['value'] = v['value'] + v['unit'] + "\n" + \
                         AIR_QUALITY_TEXT(v['grade'])
        field['short'] = "true"
        fields.append(field)
    fields.append(field)

    a_dict['fields'] = fields

    attachments.append(a_dict)
    return attachments




if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose


if slack_client.rtm_connect():
    print("StarterBot connected and running!")
    while True:
        command, channel = parse_slack_output(slack_client.rtm_read())

        if command and channel:
            handle_command(command, channel)

        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print("Connection failed. Invalid Slack token or bot ID?")

