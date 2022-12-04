import json
import os
import socket
import sys
import time
from pathlib import Path

import tweepy
from dotenv import find_dotenv, load_dotenv
from flatten_json import flatten

# from kafka import KafkaProducer



class TweetGatherer():
    def __init__(self, kafka=None, rel_env_path=None, abs_env_path=None, hashtags: list = None):

        # ========================== setup ==========================

        self.env_path = None
        if rel_env_path:
            self.env_path = Path('../.env')    
        elif abs_env_path:
            self.env_path
        load_dotenv(dotenv_path=self.env_path)
        
        
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        self.client = tweepy.StreamingClient(bearer_token=self.bearer_token)
        self.client.on_data = self.on_data
        self.hashtags = hashtags
        self.rules = [
            tweepy.StreamRule(value="has:images has:hashtags -is:retweet #football", tag="rulseset1", id=1),
            tweepy.StreamRule(value="has:images has:hashtags -is:retweet #corn #maze", tag="rulseset1", id=2),
        ]
        
        self.NUM_TWEETS = 100  # how many tweets to harvest
        self.TWEET_COUNT = 0

        self.kafka = kafka

    def add_rules(self, dry_run=False):
        # If running we need to grab whatever rules are already present.
        if self.client.running:
            pass
        elif not self.client.running:
            self.client.add_rules(add=self.rules, dry_run = dry_run)
            return 1
        else:
            return 0
        
    def update_rules(self, dry_run=False):
        # To update rules we must delete all present rules, and reignite them
        rules = [i.id for i in tw.client.get_rules().data]
        self.client.delete_rules(rules)
        self.add_rules()
        return
        
    def add_hashtags(self, hashtag):
        # get current hastags:
        rules = [i for i in tw.client.get_rules().data]
        hashtags = []
        for rule in rules:
            for h in rule.value.split():
                if h.startswith('#'):
                    hashtags.append(h)
                    
        # add new hastags:
        if type(hashtag) is list: 
            for tag in hastag:
                hashtags.append(tag)
        else:
            hashtags.append(hashtag)
        
        # update ruleset with all hastags:
        l = ' '.join(hashtags)
        self.rules = [
            tweepy.StreamRule(value=f"has:images has:hashtags -is:retweet {l}", tag="rulseset1"),
        ]
        print(self.rules)
        
     
        
    def on_data(self, json_data):
        """Tweepy calls this when it receives data from Twitter"""
        json_obj = json.loads(json_data.decode())
        json_str = json.dumps(json_obj)
        json_bytes = json_str.encode()
        
        print(f'Received tweet {self.TWEET_COUNT}')
        print(json.dumps(json_obj, indent=4))
        self.TWEET_COUNT += 1
        if self.TWEET_COUNT >= self.NUM_TWEETS:
            self.__on_finish()

        flattened = flatten(json_obj)
        if 'data_attachments_media_keys_0' in flattened.keys():
            print(json.dumps(json_obj, indent=4))
    def __on_finish(self):
        self.client.disconnect()

        print('Stopped!')
        
    def run(self):
        
        self.client.filter()
            
tw = TweetGatherer()
# print(tw.add_hashtags(['sdaf']))
# print(rules)
# tw.client.delete_rules()
# tw.update_rules()
tw.add_hashtags('new')

