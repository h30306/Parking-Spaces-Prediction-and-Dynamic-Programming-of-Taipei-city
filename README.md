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

## Train your own LSTM model 

1. Unzip model_training/data/parking_data_all_V3.csv.zip and model_training/data/Google_api_V1.csv.zip
2. Run model_training/model/preprocessing.py for preprocessing csv data to pickle
```
python ./model_training/model/preprocessing.py
```
3. Train LSTM model
```
python ./model_training/model/LSTM.py
```
4. Move the new LSTM model to prediction model folder
```
mv ./model_training/model/lstm_model.h5 ./parking_map/lstm_model.h5
```
