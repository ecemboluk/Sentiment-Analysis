# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tweepy as tw
import pandas as pd

consumer_key = "GzxtX84ZQDNvN21FXjvWJLkey"
consumer_secret = "29kx6aikg4BVTXIv1Z20ABRAC5jlJAjG5jbucWHRFSfB84AsGi"
access_token = "166684447-yNqEZidmt780xpPNEgqdVwlm5W39xPOtfZpXesM4"
access_token_secret = "OLk3qeytGvBj6bkpBnEsy4OW85mNBh0Hf0TQkk74SKmwV"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)

search_term = ["@TK_HelpDesk -filter:reply","@pegasusdestek - filter:reply","@AJ_Destek -filter:reply","@SunExpress -filter:reply"]
passanger_tweet = []
company = []


for term in search_term:
    tweets = tw.Cursor(api.search,
                   q=term,
                   lang="tr",
                   tweet_mode='extended',).items()
    if len(passanger_tweet)==0:
        passanger_tweet = [[tweet.full_text] for tweet in tweets]
    else:
        for tweet in tweets:
            passanger_tweet.append([tweet.full_text])

df = pd.DataFrame(data= passanger_tweet, columns=['tweet'])
df.to_csv('tweet_last.csv', sep=',', encoding='utf-8',index=False) 
