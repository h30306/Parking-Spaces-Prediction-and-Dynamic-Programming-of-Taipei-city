import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras import optimizers
from keras.layers import LSTM
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from keras.models import load_model
import os
os.listdir()

parking_data = pd.read_pickle("../data/parking_data.pkl")

parking_data = parking_data.drop(['availablecar', 'updatetime', 'date', 'time'], axis=1)
parking_data.fillna(-1, inplace=True)


parking_data = parking_data[parking_data['availablecar_next_percentage'] > 0]

def buildTrain(train, pastDay=6, futureDay=3):
    X_train, Y_train = [], []
    for p_id in list(set(list(train['park_id']))):
        train_sub = train[train['park_id'] == p_id]
        for i in range(train_sub.shape[0]-futureDay-pastDay):
            X_train.append(np.array(train_sub.iloc[i:i+pastDay, 1:]))
            Y_train.append(np.array(train_sub.iloc[i+pastDay:i+pastDay+futureDay]["availablecar_next_percentage"]))
    return np.array(X_train), np.array(Y_train)

print('##### Building Train Data #####')
X, Y = buildTrain(parking_data, pastDay=6, futureDay=3)
Y = Y.reshape(Y.shape[0] ,Y.shape[1], 1)
print(X.shape)
print(Y.shape)
print('##### Done Building Train Data #####')

model = load_model('lstm_model.h5')
print('evatuate: ',model.evaluate(X, Y))
