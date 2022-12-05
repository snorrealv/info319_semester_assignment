from transformers import pipeline

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import os
# code inspired by https://github.com/christianversloot/machine-learning-articles/blob/main/easy-object-detection-with-python-huggingface-transformers-and-machine-learning.md

import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import requests
import json
from kafka import KafkaProducer, KafkaConsumer

url = 'http://images.cocodataset.org/val2017/000000039769.jpg'

class HashtagExtractor:
    def __init__(self):
    
        self.filename = 'temp.jpg'
        self.filepath = None
        self.img_processed = None

        # Misc
        self.temporary_images = '../data/temporary_images/'
        self.__is_cleaned = False

    # def get_content(self, url):
    #     # Downloads the image for processing.
    #     img_data = requests.get(url).content
    #     self.filepath = self.temporary_images + self.filename

    #     with open(self.filepath, 'wb') as handler:
    #         handler.write(img_data)
        
    # def delete_image(self):
    #     os.remove(self.filepath)
    
    # Open the image
    def find_hastags(self, url):
        image = Image.open(requests.get(url, stream=True).raw)

        feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
        model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits
        # model predicts one of the 1000 ImageNet classes

        l = [t.detach().numpy() for t in torch.topk(logits, 5)]
        print(l[0])
        print(l[1])
        hashtags = {}
        for i in range(len(l[0][0])):
            tags = model.config.id2label[l[1][0][i]]
            tags = tags.replace(',', '')
            tags = tags.split()
            tags = ['#'+tag for tag in tags]
            print("Predicted class:", tags, 'score:', l[0][0][i])
            for tag in tags:
                hashtags[tag]=str(l[0][0][i])
        
        return {'implicit_hashtags':hashtags}

HOST = 'localhost'
producer = KafkaProducer(bootstrap_servers='localhost:9092')
PORT = 65000

consumer = KafkaConsumer('tweets2', bootstrap_servers='localhost:9092')
hs = HashtagExtractor()

for msg in consumer:
    json_obj = json.loads(msg.value.decode())
    #json_str = json.dumps(json_obj)
    try:
        print(json_obj['includes_media_0_url'])
        print('TRAIN')
        results = hs.find_hastags(json_obj['includes_media_0_url'])
        
        # find hashtags:
        text = json_obj['data_text']
        explisit_hashtags = [ t for t in text.split() if t.startswith('#') ]
        
        # Create payload
        results['tweet_id'] = json_obj['data_id']
        results['explicit_hashtags']=explisit_hashtags
        print(results)
        
        # send
        print('SEND')
        json_str = json.dumps(results)
        json_bytes = json_str.encode()
        producer.send('hash_tweets', json_bytes)
    except Exception as e:
        print(e)

# hs.find_hastags('http://t2.gstatic.com/licensed-image?q=tbn:ANd9GcQOO0X7mMnoYz-e9Zdc6Pe6Wz7Ow1DcvhEiaex5aSv6QJDoCtcooqA7UUbjrphvjlIc')