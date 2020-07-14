import requests
import flask
from flask import jsonify, request
from flask import render_template
from bs4 import BeautifulSoup
from selenium import webdriver
import re
# import pandas as pd
import folium
from predict import predict_parking


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

def traffic(location):
    '''計算兩地點之間(路線)的距離與時間'''
    #global demo
    print(location)
    demo = predict_parking(location)#location
    t = []
    m = []
    loc_gm = str(loc).replace('[', '').replace(']', '')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='/Users/star/chromedriver')

    for i in range(0, len(demo['park_id'])):
        browser.get('https://www.google.com.tw/maps/dir/'+str(loc_gm)+'/'+str(demo['lat'][i])+','+str(demo['lon'][i])+'/data=!3m1!4b1!4m2!4m1!3e0')
        soup = BeautifulSoup(browser.page_source, "html.parser")
        minute = soup.find_all("div", class_ = "section-directions-trip-numbers")
        while not minute:             
            browser.get('https://www.google.com.tw/maps/dir/'+str(loc)+'/'+str(demo['lat'][i])+','+str(demo['lon'][i])+'/data=!3m1!4b1!4m2!4m1!3e0')
            soup = BeautifulSoup(browser.page_source, "html.parser")
            minute = soup.find_all("div", class_ = "section-directions-trip-numbers")
        for c, k in enumerate(minute):
            t.append("".join(re.findall('\d+\D{,5}',
                                         k.find("div", class_="section-directions-trip-duration").text)).rstrip(" ").replace("\xa0", " ").split(" ")[0])
            m.append("".join(re.findall('\d+\D{,3}',
                                        k.find("div", class_="section-directions-trip-distance").text.strip(" ").replace(",", "."))).replace("\xa0", " ").split(" ")[0])

            if c == 0:
                break

    browser.close()
    demo['minute'] = t
    demo['km'] = m
    return demo

# 使用folium來繪製路線圖
def map():
    demo1 = demo
    # def combine(row):
    #     return [row['lat'], row['lon']]
    # demo1['point']=demo1.apply(combine, 1)
    demo1['point'] = [[demo1['lat'][i], demo1['lon'][i]] for i in range(len(demo1['lat']))]

    # 創建基本Map
    m = folium.Map(demo1['point'][0],zoom_start=15 , tiles='http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga',attr='Google')  #中心區域的確定

    # 繪製標地點並顯示路線順序與地址等
    for i in range(0, len(demo1)):
        label =  '名稱: ' + str(demo1['name'][i]) + '<br>可用停車位: ' + str(demo1['availible'][i])+\
        '<br>10分鐘: ' + str(demo1['ten_minute'][i]) + '<br>20分鐘: ' + str(demo1['twenty_minute'][i])+ '<br>30分鐘: ' + str(demo1['thirty_minute'][i])  
        popup = folium.Popup(label,max_width=300,min_width=300)
        folium.Marker(demo1['point'][i], popup=popup).add_to(m)

    return m.get_root().render()

@app.route('/parking_map', methods=['POST'])
def run():
    print('hi!!!')
    if request.method == 'POST':
    #if 'query' in request.args:
        location = request.values
    demo = traffic(location['location'])
    map_result = map()

    return {'info':demo, 'map_html':map_result}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) #change the port you want to start prediction model server