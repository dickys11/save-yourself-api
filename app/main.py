from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import config
import schemas
import json

def getapi():
    try:
        tapi = config.createAPI()
        yield tapi
    except Exception as e:
        print(f'[-] {e}')

app = FastAPI()

@app.get('/getstatus/{uname}', response_model=schemas.Tweet)
def getstatus(uname, api = Depends(getapi)):
    user_timeline = api.user_timeline(uname, tweet_mode="extended")
    username = uname
    tweet_list = []
    tweet_dict  = {}
    for tweet in user_timeline:
        tweet_dict['created_at'] = tweet._json['created_at']
        tweet_dict['text'] = tweet._json['full_text']
        tweet_dict_copy = tweet_dict.copy()
        tweet_list.append(tweet_dict_copy)

    result = {
        'username': username,
        'tweet': tweet_list
    }
    return result
