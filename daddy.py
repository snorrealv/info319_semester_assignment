from scripts import object_detection, tweet_gather_tweepy
import multiprocessing
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv

def hash_extract():
    hs = object_detection.HashtagExtractor(
                        producer_topic_implicit='tweets_implicit',
                        producer_topic_explicit='tweets_explicit',
                        consumer_topic='tweets',
                        ip='127.0.0.1',
                        port='9092')
    hs.run()
    return 0

def tweet_gather():
    # Get Bearer token
    env_path = Path('.env')    
    load_dotenv(dotenv_path=env_path)
    bearer_token = os.environ.get("BEARER_TOKEN")
    
    tw = tweet_gather_tweepy.TweetGatherer(
                    ip='127.0.0.1',
                    port='9092',
                    topic='tweets',
                    bearer_token=bearer_token)
    tw.run()
    return 0



if __name__ == '__main__':
    tweet = multiprocessing.Process(name='tweet', target=tweet_gather)
    hash_e = multiprocessing.Process(name='hash_e', target=hash_extract)
    tweet.start()
    hash_e.start()