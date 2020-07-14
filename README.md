# Parking-spaces-prediction-of-Taipei-city

## Introduction

This is a website that can get your location (Only for Taipei City) and predict the number of remaining parking spaces in the nearby parking lot in the next 30 minutes, and calculates the best route to each parking lot using the Google API, reducing the time for waiting for parking spaces. 

## Require

- python>=3
- Apache
- Two Server (For deploy the website and the prediction model)
- Tensorflow<2
- keras 2.3.1

## Start Up

1. Change the sys.path in website/app.wsgi to your own Apache website path<br>
2. Change line 37 in webiste/server.py to your prediction model server address and port<br>
3. Launch the website by Apache<br>
4. Change line 86 in parking_map/map.py to the same port as the website/server.py<br>
5. Launch the prediction model<br>
```
python ./parking_map/map.py
```
6. Now you can open the website for checking the nearby parking spaces<br>
