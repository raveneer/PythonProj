
import os
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    
    #멤버 초기화
    logdir = '.'
    keys = []
    watch_files = {'file_name':'file_offset'}
    slack_client = None
    slack_channel= ''
    
    
    def __init__(self, slack) :
        self.slack_client = slack
        return

    def set_param(self, keys, channel_name):
        self.keys = keys[:]
        self.slack_channel = channel_name


    def on_modified(self, event):
        if event.event_type == 'modified' and not event.is_directory :
            if event.src_path in self.watch_files :
                self.do_monitoring_file(event)
            else:
                self.watch_files[event.src_path] =  os.path.getsize(event.src_path)

    def do_monitoring_file(self, event):
        modify_content = self.get_modify_content(event)
        content_list = modify_content.split('\n')

        for line in content_list:
            for token in self.keys :
                if line.find(token) > 0:
                    self.slack_client.api_call("chat.postMessage", channel=self.slack_channel, text='FILE MONITORING\n{0}'.format(line), as_user=True)
                    break

    def get_modify_content(self, event):
        last_pos = self.watch_files[event.src_path]
        current_pos = os.path.getsize(event.src_path)
        self.watch_files[event.src_path] = current_pos

        event_file = open(event.src_path, 'r')
        event_file.seek(last_pos)
        modify = event_file.read(current_pos)
        event_file.close()
        return  modify









