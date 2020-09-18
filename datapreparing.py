#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 12:07:58 2020

@author: ecem
"""

import numpy as np
import pandas as pd
import re
import string
from turkishdeasciifier.turkish.deasciifier import Deasciifier
import nltk
from collections import Counter

counter = 0

# Remove Punctuations

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

# Remove Number
    
def remove_numbers(text):
    text = ''.join([i for i in text if not i.isdigit()])         
    return text

# Remove URL
    
def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)

# Remove HTML Tags
    
def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)

# Remove Emoji
    
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags 
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

#regular expression

def tr_lower(self):
    self = re.sub(r"İ", "i", self)
    self = re.sub(r"I", "ı", self)
    self = re.sub(r"Ç", "ç", self)
    self = re.sub(r"Ş", "ş", self)
    self = re.sub(r"Ü", "ü", self)
    self = re.sub(r"Ö", "ö", self)
    self = re.sub(r"Ğ", "ğ", self)
    self = self.lower() 
    return self

data = pd.read_csv("annotation_data.csv")
data.drop(["annotation_approver","id","user"],axis=1,inplace=True)

sentiment = [0 if s == 11 else 1 for s in data.label]
array_s = np.array(sentiment)
tweet = data.loc[:,"text"]

#replace string

tweet = tweet.str.replace("@TK_TR"," ")
tweet = tweet.str.replace("@TK_HelpDesk"," ")
tweet = tweet.str.replace("@BilalEksiTHY"," ")
tweet = tweet.str.replace("@Airbus"," ")
tweet = tweet.str.replace("@RT"," ")
tweet = tweet.str.replace("RT"," ")
tweet = tweet.str.replace("@TurkishAirlines"," ")
tweet = tweet.str.replace("@THY_Teknik"," ")
tweet = tweet.str.replace("#thy"," ")
tweet = tweet.str.replace("@pegasusdestek"," ")
tweet = tweet.str.replace("@ucurbenipegasus"," ")
tweet = tweet.str.replace("@AJ_Destek"," ")
tweet = tweet.str.replace("@flymepegasus"," ")
tweet = tweet.str.replace("@dhmiucusbilgi "," ")
tweet = tweet.str.replace("#PegasusHavayolları "," ")
tweet = tweet.str.replace("@CoronaTurkey"," ")
tweet = tweet.str.replace("@SunExpress "," ")
tweet = tweet.str.replace("@OnurAir"," ")

for t in tweet:
    t = remove_punct(t)
    t = remove_numbers(t)
    t = remove_URL(t)
    t = remove_html(t)
    t = remove_emoji(t)
    t = tr_lower(t)
    t = t.lower()
    tweet[counter] = t
    counter = counter +1

counter = 0
    
# Deascify    
    
for t in tweet:
    deasciifier = Deasciifier(t)
    t = deasciifier.convert_to_turkish()
    tweet[counter] = t
    counter = counter +1 

# tokenize

tweet_list = []
word_list = []
tokenize_list = []
for t in tweet:
    twt = nltk.word_tokenize(t)
    tokenize_list.append(twt)
    for word in twt:
        word_list.append(word)
    twt = " ".join(twt)
    tweet_list.append(twt)
      

# Create Vocab 

counts = Counter(word_list)
vocab = sorted(counts, key=counts.get, reverse=True)

for v in vocab:
    if len(v) == 1:
        vocab.remove(v)
        
vocab_to_int = {word: ii for ii, word in enumerate(vocab, 1)}
print("Maximum tweet length: {}".format(len(max(tokenize_list))))


#Encode the words

tweets_ints = [] 
for tweet in tweet_list:     
    tweets_ints.append([vocab_to_int[word] if word in vocab_to_int else 0 for word in tweet.split()])

#Padding sequences

def pad_features(tweets_ints, seq_length):
    
    features = np.zeros((len(tweets_ints), seq_length), dtype=int)
    for i, row in enumerate(tweets_ints):
        features[i, -len(row):] = np.array(row)[:seq_length]
        
    return features

seq_length = len(max(tokenize_list))

features = pad_features(tweets_ints, seq_length=seq_length)

assert len(features)==len(tweets_ints)
assert len(features[0])==seq_length


















