Bot Builder takes a zulip username and api key, a word or phrase to respond to, a search string for giphy, an optional caption or list of captions, and a list of the zulip streams it should be active in. it then posts a caption and a randomly selected gif in response to zulip messages.


At the bottom of Bot Builder you can change a few settings to customize your bot.

- zulip_username and zulip_api_key are given to you when you create a zulip bot. You can do this in Zulip -> Settings

- key_word is the text in Zulip you would like the bot to respond to. This may be a 
        single word or a phrase.

- search_string is what you want the bot to search giphy for.

- caption may be one of: [] OR 'a single string' OR ['or a list', 'of strings']

- subscribed_streams is a list of the streams the bot should be active on. An empty 
        list defaults to ALL zulip streams
