# -*- coding: utf-8 -*

import pandas as pd
import numpy as np
import geocoder
from math import radians, cos, sin, asin, sqrt
import os
import re
from datetime import datetime
import mysql.connector
import mysql
import json
from keras.models import load_model
os.listdir()


def list_col(mycursor, table_name):
    mycursor.execute("SHOW columns FROM {}".format(table_name))
    col_name_list = [column[0] for column in mycursor.fetchall()]
    return col_name_list

def list_table(mycursor):
    mycursor.execute("show tables")
    table_list = [tuple[0] for tuple in mycursor.fetchall()]
    return table_list

def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

def predict_parking(input_location):
    mydb = mysql.connector.connect(
            host="demo.jlwu.info",       
            user="BD1082A",   
            passwd="@DBrl8kVLg9g9QRiD",
            database="BD1082A",
            port=1107
        )
    mycursor = mydb.cursor()
    post_data = {}
    ##### 以parking_info計算一公里內的停車場 #####
    mycursor.execute("select * from parking_info")
    parking_info = mycursor.fetchall() 
    parking_info = pd.DataFrame(parking_info, columns=['park_id', 'city', 'area', 'tw97x', 'tw97y', 'name', 'address', 'type1', 'payex', 'tel', 'totalcar', 'totalmotor', 'totalbike', 'totalbus', 'servicetime', 'updatetime', 'summary'])

    parking = []
    for i,v in parking_info.iterrows():
        if haversine(input_location[0], input_location[1], v['tw97x'], v['tw97y']) < 1000:
            parking.append(v['park_id'])
        else:
            continue

    parking = parking_info[parking_info['park_id'].isin(parking)]

    if len(parking) == 0:
        return '附近沒停車場'
    
    ##### predict LSTM #####
    parking_data = pd.read_pickle("parking_data_subset.pkl")
    parking_data.reset_index(drop=True, inplace=True)

    now = datetime.now()
    dt = int(now.strftime("%H%M"))

    #找時間點
    index = []
    for i in list(parking['park_id']):
        temp = parking_data[parking_data['park_id'] == int(i)]
        for j in list(temp.index)[:-1]:
            if (int(temp.loc[j]['time']) <= dt):
                if (int(temp.loc[j+1]['time']) >= dt):
                    index.append(j)
                    break

    parking_data = parking_data.drop(['availablecar', 'updatetime', 'date', 'time'], axis=1)

    #建立預測資料
    X_train=[]
    for i in index:
        X_train.append(np.array(parking_data.iloc[i-6:i, 1:]))

    #預測
    lstm = load_model("lstm_model1.h5")
    result = lstm.predict(np.array(X_train))

    #轉換回停車位
    ten = [int(a*b) for a,b in zip(np.maximum(result[:,0,:].ravel(), 0).tolist(), list(parking['totalcar'].astype(float)))]
    twenty = [int(a*b) for a,b in zip(np.maximum(result[:,1,:].ravel(), 0).tolist(), list(parking['totalcar'].astype(float)))]
    thirty = [int(a*b) for a,b in zip(np.maximum(result[:,2,:].ravel(), 0).tolist(), list(parking['totalcar'].astype(float)))]

    ##### 全部包成JSON #####
    post_data['park_id'] = list(parking['park_id'])
    post_data['name'] = list(parking['name'])
    post_data['address'] = list(parking['address'])
    post_data['lat'] = list(parking['tw97y'])
    post_data['lon'] = list(parking['tw97x'])
    post_data['payex'] = list(parking['payex'])
    post_data['totalcar'] = list(parking['totalcar'])
    post_data['servicetime'] = list(parking['servicetime'])
    post_data['summary'] = list(parking['summary'])
    post_data['ten_minute'] = ten
    post_data['twenty_minute'] = twenty
    post_data['thirty_minute'] = thirty

    return post_data
