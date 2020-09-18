#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:28:06 2020

@author: ecem
"""

import datapreparing as dp
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


# Train Test Split

train_x, test_x, train_y, test_y = train_test_split(dp.features, dp.array_s, test_size = 0.2, random_state = 42)

print("train_x shape: ",train_x.shape)
print("train_y shape: ",train_y.shape)
print("test_x shape: ",test_x.shape)
print("test_y shape: ",test_y.shape)

# Create Model

max_feature = len(dp.vocab) #number of word

model = Sequential()

# Embedding layer
model.add(Embedding(max_feature+1,14,input_length=dp.seq_length))
# Recurrent layer
model.add(LSTM(40))
# Output layer
model.add(Dense(1, activation='sigmoid'))
# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_x, train_y.reshape(-1,1), epochs = 10)
y_head = model.predict(test_x)
score,acc = model.evaluate(test_x, test_y.reshape(-1,1))
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))

yhat_classes = model.predict_classes(test_x)

yhat_classes = yhat_classes[:, 0]

cm_test = confusion_matrix(test_y,yhat_classes)

