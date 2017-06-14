#-*- coding: utf-8 -*-
import json
import requests
import logging
import subprocess


api_key = "jesIR41SPZnxR6T%2FeGyEfaj9KThVoglsiAvgOtBsZoH%2FYpNHmq%2BRi5kmRs0RmWHzhfAZphbOkBr5f75M%2FBpd%2Fg%3D%3D"

class AirKorea(object):

    def __init__(self, token):
        self.token = token
        self.base_url = "http://openapi.airkorea.or.kr/openapi/services/rest"

    def forecast(self, sidoName):
        resource_path = "/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"
        params = "sidoName=" + sidoName + "&pageNo=1&numOfRows=40&ServiceKey=" + self.token + "&ver=1.3&_returnType=json"
        service_url = self.base_url + resource_path + params
        r = requests.get(service_url)

        if r.status_code == 200:
            return r.text
        else:
            return "error"

def execute_air_info():
    #무조건 영등포구의 미세먼지 정보를 얻도록 한다.
    airkorea = AirKorea(api_key)
    response = airkorea.forecast('서울')
    response = json.loads(response)
    if ('list' not in response) or (len(response['list']) == 0):
        return "not_exist"

    for station in response['list'] :
        if station['stationName']== '영등포구' :
            air_info = station
            break
        #end if
    #end for

    logging.info(air_info)

    #여기서 부터 슬랙에 뿌려주는 내용을 만들어 준다
    attachments = []
    a_dict = {}
    a_dict['title'] = air_info['stationName'] + "의 대기질 정보 입니다."
    a_dict['mrkdwn_in'] = ["text", "pretext"]

    fields = []
    #종합지수 넣기
    total_field = {
        "title": '종합지수',
        "value": air_info['khaiValue'] + "점"

    }
    fields.append(total_field)

    #미세먼지 넣기
    pm10field = {}
    pm10field['title'] = '미세먼지'
    pm10field['value'] = air_info['pm10Value']
    pm10field['short'] = "true"
    fields.append(pm10field)

    #초미세먼지
    pm25field ={}
    pm25field['title'] = '초미세먼지'
    pm25field['value'] = air_info['pm25Value']
    pm25field['short'] = "true"
    fields.append(pm25field)

    a_dict['fields'] = fields
    attachments.append(a_dict)
    return attachments

#프로젝트 이름을 주면 빌드를 한다.
nant_bin = 'E:\\Program Files\\nant-0.92\\bin\\nant.exe'
ngf_proj_xml = '-buildfile:D:\\NGF_FULL\\Branches\\swkim_brach\\AutoBuild\\Nant Script\\ngf_release.xml'
ngf_build_log  = '-logfile:d:\\NGF_FULL\\trunk\\autobuild\\_logs\\slackbot.log'
dof_proj_xml = '-buildfile:D:\\NGF_FULL\\Branches\\swkim_brach\\AutoBuild\\Nant Script\\dof_release.xml'
dof_build_log  = '-logfile:d:\\NGF_FULL\\trunk\\autobuild\\_logs\\slackbot.log'

def execute_auto_build(slack_client, channel, projName) :

    slack_client.api_call("chat.postMessage", channel=channel, text='{0} 제품 빌드를 시작 합니다.'.format(projName), as_user=True)

    if projName == 'ngf' :
        cmd = subprocess.call([nant_bin, ngf_proj_xml, 'build', ngf_build_log])
    else :
        cmd = subprocess.call([nant_bin, dof_proj_xml, 'build', dof_build_log])

    attachments_dict = dict()
    attachments_dict['pretext'] = '{0} 제품이 빌드되었습니다'.format(projName)
    attachments_dict['title'] = '{0} 제품이 빌드되었습니다'.format(projName)
    attachments_dict['fallback'] = '{0} 제품이 빌드되었습니다'.format(projName)
    attachments_dict['text'] = "제품 빌드 완료"
    attachments_dict['mrkdwn_in'] = ["text", "pretext"]
    attachments = [attachments_dict]

    return attachments






