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
from keras.models import load_model
from keras.callbacks import EarlyStopping
from keras.models import load_model
import os
os.listdir()

parking_data = pd.read_pickle("../data/parking_data.pkl")

parking_data = parking_data.drop(['availablecar', 'updatetime', 'date', 'time'], axis=1)
parking_data.fillna(-1, inplace=True)

# p_o = parking_data
# p_o = p_o.fillna(-1)
# parking_data = p_o.loc[:100000]

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

indices = np.random.permutation(X.shape[0])
rand_data_x = X[indices]
rand_data_y = Y[indices]

X_train, X_test, y_train, y_test = train_test_split(rand_data_x, rand_data_y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

model = Sequential()
model.add(LSTM(200, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(RepeatVector(3))
model.add(LSTM(200, activation='relu', return_sequences=True))
model.add(LSTM(200, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(1)))
adam = optimizers.Adam(lr=0.0001, decay=1e-6, beta_1=0.9, beta_2=0.999)
model.compile(loss='mse', optimizer=adam)

early_stopping = EarlyStopping(monitor='val_loss', patience=15, verbose=2)
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=1000, verbose=1, batch_size=50, callbacks=[early_stopping])#, callbacks=[early_stopping]

test_output = model.predict(X_test, verbose=0)

print('evatuate: ',model.evaluate(X_test, y_test))
print('##### Saving model #####')
model.save('lstm_model.h5')
