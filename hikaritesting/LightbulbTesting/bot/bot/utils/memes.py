import random
import requests
import praw as p


class Meme:
    global reddit
    reddit = p.Reddit(client_id='7gZghVq_G973pA',
                         client_secret='0llvlOaEUfzZaFvHVJ6GS2NKg27yew',
                         user_agent='Red.py')
    CLIENT_ID = "7gZghVq_G973pA"
    SECRET_KEY = "0llvlOaEUfzZaFvHVJ6GS2NKg27yew"
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': 'Coler21gamer',
        'password': 'U289ulso'
    }
    headers = {'User-Agent': 'RedBotAPI/1.0.0'}
    res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    TOKEN = res.json()
    headers['Authorization'] = f'bearer {TOKEN}'
    res = requests.get('https://oauth.reddit.com/r/python/wholesomememes/', headers=headers)
    res.json

    def rando_meme(sub):
        memes_submissions = reddit.subreddit(f'{sub}').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        return submission