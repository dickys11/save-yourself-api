from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import config
import schemas
import functions
import json
import math

def getApi():
    try:
        tapi = config.createAPI()
        yield tapi
    except Exception as e:
        print(f'[-] {e}')

app = FastAPI()

@app.get('/getstatus/{uname}/{numtweet}', response_model=schemas.Tweet)
def getStatus(uname: str, numtweet: int, api = Depends(getApi)):
    username = uname
    tweet_list = []
    
    num_page = math.ceil(numtweet/20)
    for page in range(num_page):
        user_timeline = api.user_timeline(uname, page=page, tweet_mode="extended")
        tweet_list += functions.makeList(user_timeline)
    
    result = {
        'username': username,
        'tweet': tweet_list
    }
    return result