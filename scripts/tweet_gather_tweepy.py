import json
import socket
import sys
import time

import tweepy
from flatten_json import flatten
from kafka import KafkaConsumer, KafkaProducer


class TweetGatherer():
    def __init__(self, port, ip, topic, bearer_token, hashtags=None):

        # ========================== setup ==========================

    
        self.ip = ip
        self.port = port
        self.topic = topic
        
        self.server = ip +':'+port 
        
        self.producer = KafkaProducer(bootstrap_servers=self.server)
        
        self.env_path = None
        self.bearer_token = bearer_token
        self.client = tweepy.StreamingClient(bearer_token=self.bearer_token)

        self.client.on_data = self.on_data
        self.hashtags = hashtags
        self.rules = [
            tweepy.StreamRule(value="has:media has:hashtags -is:retweet (#corn OR #music OR #dog OR #ye OR #morning OR #kpop)", tag="rulseset1", id=2),
            tweepy.StreamRule(value="has:media has:hashtags -is:retweet (#football OR #ye OR #usa OR #USA)", tag="rulseset2", id=1),

        ]
        
        self.NUM_TWEETS = 100  # how many tweets to harvest
        self.TWEET_COUNT = 0

    def add_rules(self, dry_run=False):
        # If running we need to grab whatever rules are already present.
        print('added rules')
        if self.client.running:
            for rule in self.rules:
                print('1')
                self.client.add_rules(add=rule, dry_run = dry_run)
        elif not self.client.running:
            for rule in self.rules:
                print('2')
                self.client.add_rules(add=rule, dry_run = dry_run)
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
            for tag in hashtag:
                hashtags.append(tag)
        else:
            hashtags.append(hashtag)
        
        # update ruleset with all hastags:
        l = 'OR'.join(hashtags)
        self.rules = [
            tweepy.StreamRule(value=f"has:media has:hashtags -is:retweet ({l})", tag="rulseset1"),
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
        payload = json.dumps(flattened)
        self.producer.send(self.topic, payload.encode())
            
    def __on_finish(self):
        self.client.disconnect()
        print('Stopped!')
        
    def run(self):
        self.client.filter(expansions=['attachments.media_keys'], media_fields=['media_key', 'type', 'preview_image_url','url'])

