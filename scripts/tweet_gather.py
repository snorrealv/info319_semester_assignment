from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
import sys

import json
import tweepy
import time
import socket
from kafka import KafkaProducer

# Relevant twitter docs pages: https://developer.twitter.com/en/docs/twitter-api/enterprise/rules-and-filtering/building-a-rule
# Inspired by: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py


class TweetGatherer():
    def __init__(self, kafka=None, rel_env_path=None, abs_env_path=None):
        # ========================== setup ==========================
        if rel_env_path:
            self.env_path = Path('../../.env')    
        elif abs_env_path:
            self.env_path
        load_dotenv(dotenv_path=self.env_path)
        
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        self.bearer_oauth = self.bearer_oauth()

        
        self.kafka = kafka
        self.rules = [
            {"value": "dog has:images", "tag": "dog pictures"},
            {"value": "cat has:images -grumpy", "tag": "cat pictures"},
        ]


    def __bearer_oauth(r):
        # Method required by bearer token authentication.

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FilteredStreamPython"
        return r


    def get_rules():
        # Method to find what rules are set for your v2 stream:

        response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=self.__bearer_oauth
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )

        print(json.dumps(response.json()))
        return response.json()


    def set_rules():
        # Method to set new rules for our v2 stream:
        
        payload = {"add": self.rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.__bearer_oauth,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        print(json.dumps(response.json()))
    
    def delete_all_rules():
        # function to delete rules if neccesary.
             
        # If no rules, we dont need to delete them.
        if self.rules is None or "data" not in self.rules:
            return None

        ids = list(map(lambda rule: rule["id"], self.rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.__bearer_oauth,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

