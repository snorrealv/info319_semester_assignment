import json
import os
from datetime import datetime

import requests
import torch
from kafka import KafkaConsumer, KafkaProducer
from PIL import Image, ImageDraw, ImageFont
from transformers import (ViTFeatureExtractor, ViTForImageClassification,
                          pipeline)


class HashtagExtractor:
    def __init__(self, producer_topic_implicit, producer_topic_explicit, consumer_topic, ip, port):
        
        self.ip = ip
        self.port = port
        
        self.server = ip +':'+port 
        
        self.producer_topic_implicit = producer_topic_implicit
        self.producer_topic_explicit = producer_topic_explicit
        self.consumer_topic = consumer_topic
        
        self.producer = KafkaProducer(bootstrap_servers=self.server)
        self.consumer = KafkaConsumer(self.consumer_topic, bootstrap_servers=self.server)
    
    # Open the image
    def find_hastags(self, url):
        image = Image.open(requests.get(url, stream=True).raw)

        feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
        model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits

        l = [t.detach().numpy() for t in torch.topk(logits, 5)]
        hashtags = {}
        for i in range(len(l[0][0])):
            tags = model.config.id2label[l[1][0][i]]
            tags = tags.replace(',', '')
            tags = tags.split()
            tags = ['#'+tag for tag in tags]
            print("Predicted class:", tags, 'score:', l[0][0][i])
            for tag in tags:
                hashtags[tag]=str(l[0][0][i])
        
        return hashtags
    
    def run(self):
        for msg in self.consumer:
            json_obj = json.loads(msg.value.decode())
            try:
                #{'tweet_id': '1600486147905519623', 'medium': '{"media_key":"3_1600486124765544449","type":"photo","url":"https://pbs.twimg.com/media/FjYRppaXgAEYiRu.jpg"}'}
                # get implicit hashtags
                q = json.loads(json_obj['medium'])
                implicit_hashtags = self.find_hastags(q['url'])
                
                # find explicit hashtags form tweet:
                #text = json_obj['data_text']
                #explicit_hashtags = [ t for t in text.split() if t.startswith('#') ]
                
                # Create payload
                tweet_id = json_obj['tweet_id']                
                
                # send implicit
                for entry in implicit_hashtags.keys():
                    data = {'tweet_id':tweet_id, 'hashtag_i':entry, 'score':implicit_hashtags[entry]}
                    
                    json_str = json.dumps(data)
                    json_bytes = json_str.encode()
                    self.producer.send(self.producer_topic_implicit, json_bytes)
                
                # send explicit
                # for entry in explicit_hashtags:
                    
                #     data = {'tweet_id':tweet_id, 'hashtag_e':entry}
                #     json_str = json.dumps(data)
                #     json_bytes = json_str.encode()
                #     self.producer.send(self.producer_topic_explicit, json_bytes)
            except Exception as e:
                print(e)


#{"implicit_hashtags": {"#Chihuahua": "10.308017", "#Italian": "5.9688463", "#greyhound": "5.9688463", "#bath": "5.8421626", "#towel": "5.8421626", "#miniature": "5.6929255", "#pinscher": "5.6929255", "#Staffordshire": "5.6562214", "#bullterrier": "5.6562214", "#bull": "5.6562214", "#terrier": "5.6562214"}, "tweet_id": "1600116942580305921", "explicit_hashtags": ["#dog", "#ScoobySays", "#HelptheHomeless", "#CharityTuesday", "#BuyABeanie", "#GiveBack"]}