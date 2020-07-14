# -*- coding: utf-8 -*

import pandas as pd
import numpy as np
import geocoder
from math import radians, cos, sin, asin, sqrt
from sklearn.decomposition import PCA
from sklearn import preprocessing
import os
import re
import time
from multiprocessing import Pool
from datetime import datetime
from tqdm import tqdm
import pickle
os.listdir()

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

def remove_unnamed(df):
    df = df.loc[ : , ~df.columns.str.contains("^Unnamed")]
    return df

def replace_by_prct(df, columns, threshold):
    dict_={}
    remove_col = []
    for i,j in dict(df[columns].value_counts()/len(df)).items():
        if j > threshold:
            dict_[i]=i
        else:
            remove_col.append(i)
            dict_[i]='other'
    df[columns] = df[columns].map(dict_)
    print(remove_col)
    print(len(remove_col))

def max_price(x):
    try:
        return max([int(s) for s in re.findall('(\d+)元', x)])
    except:
        return -1

def softmax(x):
    """Compute the softmax in a numerically stable way."""
    x = x - np.max(x)
    exp_x = np.exp(x)
    softmax_x = exp_x / np.sum(exp_x)
    return softmax_x

def date_cmp(first_time, second_time):
    #first > second = 1 else 0
    return datetime.datetime.strptime(first_time, '%Y/%m/%d') > datetime.datetime.strptime(second_time, '%Y-%m-%d')

def activity_nearby(df):
    #產生[(activity_index, weight), ...]
    def apply_row(row):
        act = []
        ll = list(activity_final['latlng'])
        for i,v in enumerate(ll):
            dist = haversine(v[1], v[0], row['tw97x'], row['tw97y'])
            if dist<1000:
                act.append((i,1/(dist/1000)))
        return act
    df['activity_nearby'] = df.apply(lambda x : apply_row(x),axis=1)
    return df

def geo(x):
    time.sleep(1)
    return geocoder.arcgis(x).latlng

def merge_time(park_id, activity_final, parking_data, parking_info):
    temp = parking_data[parking_data['park_id'] == park_id]
    act_list = list(parking_info[parking_info.park_id == park_id]['activity_nearby'])[0]

    if len(act_list) > 0:
        for act in act_list:
            index = act[0]
            weight = act[1]
            activity_info = activity_final.loc[index]
            temp['open_date_match'] = temp['date'].apply(lambda x: 1 if int(x) >= int(activity_info['date_open']) else 0)
            temp['close_date_match'] = temp['date'].apply(lambda x: 1 if int(x) <= int(activity_info['date_close']) else 0)
            temp['open_time_match'] = temp['time'].apply(lambda x: 1 if int(x) >= int(activity_info['time_open']) else 0)
            temp['close_time_match'] = temp['time'].apply(lambda x: 1 if int(x) <= int(activity_info['time_close']) else 0)
            temp['match'] = temp['open_date_match'] + temp['close_date_match'] + temp['open_time_match'] + temp['close_time_match']
            match = temp[temp['match'] == 4]
            match['pca1'] += activity_info['activity_pca1']*weight
            match['pca2'] += activity_info['activity_pca2']*weight
            temp = match.combine_first(temp)
            temp = temp.drop(['open_date_match', 'close_date_match', 'open_time_match', 'close_time_match', 'match'], axis=1)
        return temp
    else:
        return temp
    

parking_info = pd.read_csv('../data/parking_info_V3.csv')
google = pd.read_csv('../data/Google_api_V1.csv')
parking_data = pd.read_csv('../data/parking_data_all_V3.csv')
activity = pd.read_csv('../data/activity_20191031_20200331_A63.csv')

parking_info = remove_unnamed(parking_info)
google = remove_unnamed(google)
parking_data = remove_unnamed(parking_data)
activity = remove_unnamed(activity)


##### activity #####

### 地址處理 ###
activity['address'] = activity['address'].apply(lambda x: x.replace("\n",""))

activity['latlng'] = activity.address.apply(lambda x: geo(x))
activity = activity.dropna(subset=['latlng'])

### 時間處理 ###
activity['time_split'] = activity['time'].apply(lambda x: x.split(' '))
activity['time_open'] = activity['time_split'].apply(lambda x: x[1].replace(":",""))
activity['time_close'] = activity['time_split'].apply(lambda x: x[4].replace(":",""))
activity['date_open'] = activity['time_split'].apply(lambda x: x[0].replace("/",""))
activity['date_close'] = activity['time_split'].apply(lambda x: x[3].replace("/",""))

### Type處理 ###
activity['activityType_split'] = activity['activityType'].apply(lambda x: x.split("／")[0])
replace_by_prct(activity, 'activityType_split', 0.1)

### Class處理 ###
activity['activityClass_split'] = activity['activityClass'].apply(lambda x: x.split("-")[0])
replace_by_prct(activity, 'activityClass_split', 0.09)

### 票價處理 ###
#取最高票價
activity['max_ticketPrice'] = activity['ticketPrice'].apply(lambda x : max_price(x))
#價格Bining
bins = [-2, 0, 300, 1000, 4000]
labels = [1,2,3,4]
activity['binning_ticketPrice'] = pd.cut(activity['max_ticketPrice'], bins=bins, labels=labels)
#dummies
data_dum = pd.get_dummies(activity[['activityType_split','activityClass_split','binning_ticketPrice']])
activity_dum = pd.DataFrame(data_dum)
#PCA
pca = PCA(n_components=2)
activity_pca = pca.fit_transform(activity_dum.values)
pickle.dump(pca, open("pca.pkl","wb"))
activity_pca = pd.DataFrame(activity_pca, columns=['activity_pca1', 'activity_pca2'])

activity_final = pd.concat([activity[['latlng', 'time_open', 'time_close', 'date_open', 'date_close']],activity_pca], axis=1)
activity_final = activity_final.dropna().reset_index(drop=True)
activity_final.to_pickle('../data/activity_final.pkl')


##### google #####

#根據type計算距離
#rating加權
google = google.replace(-1,0)
google['weight'] = google.apply(lambda x: x['rating']*x['user_ratings_total'], axis=1)

#算距離<1000m
google = google[['park_id', 'type', 'loc_lat', 'loc_lng', 'weight']]
parking_lnglat = parking_info[['park_id', 'tw97x', 'tw97y']]
google = pd.merge(google, parking_lnglat, on='park_id')
google['distance'] = google.apply(lambda x: haversine(x['loc_lng'], x['loc_lat'], x['tw97x'], x['tw97y']), axis=1)
google = google[google['distance'] < 1000].reset_index(drop=True)

#距離倒數當作權重
google['distance'] = google['distance'].apply(lambda x: 1/(x/1000))
google['weight'] = google.apply(lambda x: x['weight']*x['distance'], axis=1)
google = google[['park_id', 'type', 'weight']]
google = google.groupby(by=['park_id','type']).mean().reset_index()
google = google.pivot(index='park_id', columns='type', values='weight')
google = google.fillna(0)
google.to_pickle("../data/google_final.pkl")

parking_data = pd.read_pickle("../data/parking_data.pkl")
activity_final = pd.read_pickle("../data/activity_final.pkl")
google_final = pd.read_pickle("../data/google_final.pkl")
activity_final = activity_final.dropna(subset=['latlng'])
##### parking_data #####

#先計算停車場附近的活動是哪幾個
n_cores = 20
df_split = np.array_split(parking_info, n_cores)
pool = Pool(n_cores)
parking_info = pd.concat(pool.map(activity_nearby, df_split))
pool.close()
pool.join()

#根據結果跟時間margin activity to parking_data
parking_data['date'] = parking_data['updatetime'].apply(lambda x:x.split(" ")[0].replace("-", ""))
parking_data['time'] = parking_data['updatetime'].apply(lambda x:x.split(" ")[1].rsplit(":",1)[0].replace(":", ""))
parking_data['pca1'] = 0
parking_data['pca2'] = 0

for i in tqdm(list(parking_info['park_id'])):
    parking_data = merge_time(i,activity_final, parking_data, parking_info).combine_first(parking_data)

#合併google data
parking_data = parking_data.merge(google, left_on='park_id', right_on='park_id')
parking_data.to_pickle("../data/parking_data.pkl")
parking_info.to_pickle("../data/parking_info.pkl")






