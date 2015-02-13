import zulip
import json
import requests
import random
import os

class bot():
    def __init__(self, zulip_username, zulip_api_key, key_word, search_string, caption='', subscribed_streams=[]):
        self.username = zulip_username
        self.api_key = zulip_api_key
        self.key_word = key_word.lower()
        self.subscribed_streams = subscribed_streams
        self.search_string = search_string.lower()
        self.caption = caption
        self.client = zulip.Client(zulip_username, zulip_api_key)
        self.subscriptions = self.subscribe_to_streams()


    @property
    def streams(self):
        if not self.subscribed_streams:
            streams = [{'name': stream['name']} for stream in self.get_all_zulip_streams()]
            return streams
        else: 
            streams = [{'name': stream} for stream in self.subscribed_streams]
            return streams


    def get_all_zulip_streams(self):
        ''' Call Zulip API to get a list of all streams
        '''
        response = requests.get('https://api.zulip.com/v1/streams', auth=(self.username, self.api_key))
        if response.status_code == 200:
            return response.json()['streams']
        elif response.status_code == 401:
            raise RuntimeError('check yo auth')
        else:
            raise RuntimeError(':( we failed to GET streams.\n(%s)' % response)


    def subscribe_to_streams(self):
        self.client.add_subscriptions(self.streams)


    def respond(self, msg):
        content = msg['content'].lower()
        if self.key_word in content:
            img_url = self.get_giphy_response()
            self.send_message(msg, img_url) 
               

    def send_message(self, msg, img_url):
        self.client.send_message({
            "type": "stream",
            "subject": msg["subject"],
            "to": msg['display_recipient'],
            "content": '{}\n{}'.format(self.caption, img_url)
            })


    def get_giphy_response(self):
        response = requests.get('http://api.giphy.com/v1/gifs/random', params=self.get_params())
        if response.status_code == 200:
            return response.json()['data']['fixed_width_downsampled_url']
        else:
            raise RuntimeError(':( we failed to GET giphy.\n{}'.format(response.json()))


    def get_params(self):
        params = {
            'api_key': 'dc6zaTOxFJmzC',
            'tag': self.search_string
        }
        return params


    def main(self):
        self.client.call_on_each_message(lambda msg: self.respond(msg))



zulip_username = 'schwarzenegger-bot@students.hackerschool.com'
zulip_api_key = 'rPO44O49qB4uPWACArd5u6tbzY42adLM'
key_word = 'in hopper' # Text in Zulip the bot should respond to
search_string = 'get to the choppa' # bot will search giphy using these terms 
caption = 'GET TO THE HOPPAAAA!!!'# Enter text here if you want a caption above the gif. Defaults to ''
subscribed_streams = ['455 Broadway', 'bot-test', 'social'] # List of streams the bot should be active in. Defaults to ALL

new_bot = bot(zulip_username, zulip_api_key, key_word , search_string, caption, subscribed_streams)
new_bot.main()
