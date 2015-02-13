import zulip
import json
import requests
import random


class bot():
    ''' bot takes a zulip username and api key, a word or phrase to respond to, a search string for giphy,
        an optional caption or list of captions, and a list of the zulip streams it should be active in.
        it then posts a caption and a randomly selected gif in response to zulip messages.
     '''
    def __init__(self, zulip_username, zulip_api_key, key_word, search_string, captions=[], subscribed_streams=[]):
        self.username = zulip_username
        self.api_key = zulip_api_key
        self.key_word = key_word.lower()
        self.subscribed_streams = subscribed_streams
        self.search_string = search_string.lower()
        self.caption = captions
        self.client = zulip.Client(zulip_username, zulip_api_key)
        self.subscriptions = self.subscribe_to_streams()


    @property
    ''' Standardizes a list of streams in the form [{'name': stream}]
    '''
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
        ''' Subscribes to zulip streams
        '''
        self.client.add_subscriptions(self.streams)


    def respond(self, msg):
        ''' checks msg against key_word. If key_word is in msg, gets a gif url,
            picks a caption, and calls send_message()
        '''
        content = msg['content'].lower()
        if self.key_word in content:
            img_url = self.get_giphy_response()
            caption = self.get_caption()
            self.send_message(msg, caption, img_url) 
               

    def send_message(self, msg, caption, img_url):
        ''' Sends a message to zulip stream
        '''
        self.client.send_message({
            "type": "stream",
            "subject": msg["subject"],
            "to": msg['display_recipient'],
            "content": '{}\n{}'.format(caption, img_url)
            })

    def get_caption(self):
        ''' Returns a caption for the gif. This is either an empty string (no caption), 
            the single string provided, or a random pick from a list of provided captions
        '''
        if not self.caption:
            return ''
        elif isinstance(self.caption, str):
            return self.caption
        else:
            return random.choice(self.caption)

    def get_giphy_response(self):
        ''' Calls the giphy API and returns a gif url
        '''
        response = requests.get('http://api.giphy.com/v1/gifs/random', params=self.get_params())
        if response.status_code == 200:
            return response.json()['data']['fixed_width_downsampled_url']
        else:
            raise RuntimeError(':( we failed to GET giphy.\n{}'.format(response.json()))


    def get_params(self):
        ''' Parameters for giphy get requests
        '''
        params = {
            'api_key': 'dc6zaTOxFJmzC',
            'tag': self.search_string
        }
        return params


    def main(self):
        ''' Blocking call that runs forever. Calls self.respond() on every message received.
        '''
        self.client.call_on_each_message(lambda msg: self.respond(msg))


''' The Customization Part!
    
    Create a zulip bot under "settings" on zulip.
    Zulip will give you a username and API key
    key_word is the text in Zulip you would like the bot to respond to. This may be a 
        single word or a phrase.
    search_string is what you want the bot to search giphy for.
    caption may be one of: [] OR 'a single string' OR ['or a list', 'of strings']
    subscribed_streams is a list of the streams the bot should be active on. An empty 
        list defaults to ALL zulip streams

'''

zulip_username = 'arnold-bot@students.hackerschool.com'
zulip_api_key = 'Q5l4MyvIWJnNZEbjSgFqLBgipF7veJst'
key_word = 'Hey Arnold!' 
search_string = 'arnold schwarzenegger' 
caption = [            
    'Your clothes, give them to me, now!',
    'Do it!',
    'If it bleeds, we can kill it',
    'See you at the party Richter!',
    'Let off some steam, Bennett',
    'I\'ll be back',
    'Get to the chopper!',
    'Hasta La Vista, Baby!',
    'Now this is the plan : Get your ass to Mars!',
    'It\'s not a tumor!',
    'You hit like a vegetarian!',
    'What the f@#k did I do wrong?!',
]

subscribed_streams = [] 

new_bot = bot(zulip_username, zulip_api_key, key_word , search_string, caption, subscribed_streams)
new_bot.main()
