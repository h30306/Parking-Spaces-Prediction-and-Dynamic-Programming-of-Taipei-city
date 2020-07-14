import requests
import flask
from flask import jsonify, request
from flask import render_template
import pandas as pd
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

#from IPython import embed

map_html = ''
info =''

@app.route('/', methods=['GET'])
def home():
    print('hhhhhhome')
    haha='hahaha'
    map_html = '''<!DOCTYPE html>\n<head>    \n    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />\n    \n        <script>\n            L_NO_TOUCH = false;\n            L_DISABLE_3D = false;\n        </script>\n    \n    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.4.0/dist/leaflet.js"></script>\n    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>\n    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.4.0/dist/leaflet.css"/>\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>\n    <link rel="stylesheet" href="https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css"/>\n    <style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>\n    <style>#map {position:absolute;top:0;bottom:0;right:0;left:0;}</style>\n    \n            <meta name="viewport" content="width=device-width,\n                initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />\n            <style>\n                #map_231cb24c09a8480ea091c1c5713810bb {\n                    position: relative;\n                    width: 100.0%;\n                    height: 100.0%;\n                    left: 0.0%;\n                    top: 0.0%;\n                }\n            </style>\n        \n</head>\n<body>    \n    \n            <div class="folium-map" id="map_231cb24c09a8480ea091c1c5713810bb" ></div>\n        \n</body>\n<script>    \n    \n            var map_231cb24c09a8480ea091c1c5713810bb = L.map(\n                "map_231cb24c09a8480ea091c1c5713810bb",\n                {\n                    center: [25.0377, 121.564439],\n                    crs: L.CRS.EPSG3857,\n                    zoom: 15,\n                    zoomControl: true,\n                    preferCanvas: false,\n                }\n            );\n\n            \n\n        \n    \n            var tile_layer_46dd5c87651d4f2497c81be6c6f1c82e = L.tileLayer(\n                "http://mt0.google.com/vt/lyrs=m\\u0026hl=en\\u0026x={x}\\u0026y={y}\\u0026z={z}\\u0026s=Ga",\n                {"attribution": "Google", "detectRetina": false, "maxNativeZoom": 18, "maxZoom": 18, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}\n            ).addTo(map_231cb24c09a8480ea091c1c5713810bb);\n        \n</script>'''
     return render_template('index.html',**locals())

@app.route('/parking_map', methods=['GET', 'POST'])
def get_parking_info():
    print('/parking_map')
    if request.method == 'POST':
        data = request.form.get('latlon')
        location = data
        print(location)


        print('dataaaa', data)
        if len(location) == 0:
            print('**************')
            return render_template('index.html')
        url = 'http://serverIP:port/parking_map' #The server address and port of the prediction model server
        myobj = {'location':location}
        req = requests.post(url, verify=False ,data= myobj, timeout=120)
        if req =='附近沒停車場':
            return render_template('index.html')
        else:
            req =json.loads(req.text)
            print('map_html',req['map_html'][0])
            print('info',req['info'])
            print('info-address',req['info'][0]['address'])
            map_html = str(req['map_html'])
            info=req['info']
            abc='123'
            return render_template('index.html',**locals())
        
        

if __name__ == "__main__":
    app.run()
