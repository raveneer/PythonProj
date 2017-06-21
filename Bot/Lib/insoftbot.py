#-*- coding: utf-8 -*-


import subprocess

class INsoftBot(object):

    def __init__(self):
        self.bot_id = ''
        self.autobuild = ''
        return

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.bot_id in output['text']:
                    return output['text'].split(self.bot_id)[1].strip().lower(), \
                           output['channel']

        return None, None

    def handle_command(self, slack_client, command, channel):
        # command를 공백으로 구분해서 목록을 만들어 보자.
        command_list = command.split()
        for command_token in command_list:
            if command_token == 'ngf빌드':
                subprocess.run(['python', '{0}\\NGFAutoBuildMain.py'.format(self.autobuild)])
                break

            if command_token == 'dof빌드':
                subprocess.run(['python', '{0}\\DOFAutoBuildMain.py'.format(self.autobuild)])
                break

            if command_token == 'agent빌드':
                subprocess.run(['python', '{0}\\AgentAutoBuildMain.py'.format(self.autobuild)], stdout=subprocess.PIPE)
                break
        # end for

        slack_client.api_call("chat.postMessage", channel=channel, text="TEST", as_user=True)

    def set_bot_id(self, slack_client, bot_name):
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == bot_name:
                    self.bot_id = '<@{0}>'.format( user.get('id') )
                    return

    def set_autobuild_root(self, root_dir):
        self.autobuild = root_dir












