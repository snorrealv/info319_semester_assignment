import json

l = {'tweet_id': '1600486147905519623', 'medium': '{"media_key":"3_1600486124765544449","type":"photo","url":"https://pbs.twimg.com/media/FjYRppaXgAEYiRu.jpg"}'}
q = json.loads(l['medium'])
implicit_hashtags = q['url']


print(implicit_hashtags)