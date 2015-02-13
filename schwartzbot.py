import zulip
import json
import requests
import random
import os

class bot():
    def __init__(self, ZULIP_USERNAME, ZULIP_API_KEY, response_string):
        self.username = ZULIP_USERNAME
        self.api_key = ZULIP_API_KEY
        self.key_word = response_string.upper().split()
        self.client = zulip.Client(ZULIP_USERNAME, ZULIP_API_KEY)
        self.streams = self.get_zulip_streams()
        self.subscriptions = self.subscribe_to_streams()

    # call Zulip API to get list of all streams
    def get_zulip_streams(self):
        response = requests.get(
            'https://api.zulip.com/v1/streams',
            auth=requests.auth.HTTPBasicAuth(self.username, self.api_key)
        )
        if response.status_code == 200:
            return response.json()['streams']
        elif response.status_code == 401:
            raise RuntimeError('check yo auth')
        else:
            raise RuntimeError(':( we failed to GET streams.\n(%s)' % response)


    # subscribe the bot to all streams
    def subscribe_to_streams(self):
        streams = [
                {'name': stream['name']}
                for stream in self.streams
            ]
        self.client.add_subscriptions(streams)


    # call respond function when client mentions "Hopper"
    def respond(self, msg):
        print "so far, so good"
        # Make sure the bot never responds to itself or it results in infinite loop
        if msg['sender_email'] != "schwartz-bot@students.hackerschool.com":
            content = msg['content'].upper()
            print content
            print self.key_word
            # bot sends message when word self.key_word appears 
            for word in self.key_word:
                    if word in content:
                        print "YES!"
                        giphy_response = requests.get('http://api.giphy.com/v1/gifs/random?tag=arnold+predator&api_key=dc6zaTOxFJmzC').json()
                        img_url = giphy_response['data']['fixed_width_downsampled_url']
                        if msg['type'] == 'stream':
                            self.client.send_message({
                                "type": "stream",
                                "subject": msg["subject"],
                                "to": msg['display_recipient'],
                                "content": "GET TO THE HOPPAAAAA!!!! \n %s" % img_url
                                })

    def get_params(self):
        query = self.normalize_query()
        print query
        params = {
            'api_key': 'dc6zaTOxFJmzC',
            'tag': query
        }
                

    # accept the content of msg split into array
    def normalize_query(self):
        query = '+'.join(self.key_word)
        return query.lower()

    def main(self):
        self.client.call_on_each_message(lambda msg: self.respond(msg))


# This is a blocking call that will run forever
# client.call_on_each_message(lambda msg: respond(msg))
schwartz = bot('schwarzenegger-bot@students.hackerschool.com', 'rPO44O49qB4uPWACArd5u6tbzY42adLM', 'Hopper')
schwartz.main()
