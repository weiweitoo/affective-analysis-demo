from flask import Flask, render_template, jsonify, request
from random import *
from flask_cors import CORS
from pathlib import Path
import requests
import boto3
import botocore
import os

if not os.path.exists(os.getcwd()+"/model/08_58_Feb_08_2020"):
    os.makedirs(os.getcwd()+"/model/08_58_Feb_08_2020")
if not os.path.exists(os.getcwd()+"/model/06_06_Feb_05_2020"):
    os.makedirs(os.getcwd()+"/model/06_06_Feb_05_2020")

s3 = boto3.resource('s3')

BUCKET_NAME = 'affective-analysis-model'
KEY = 'model/'
KEY_1 = 'model/06_06_Feb_05_2020/'
KEY_2 = 'model/08_58_Feb_08_2020/'

def downloadFromS3(bucket, key, filename, output_path):
    try:
        print(output_path + filename)
        s3.Bucket(bucket).download_file(key + filename, output_path + filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

downloadFromS3(BUCKET_NAME, KEY, 'label_encoder.pkl', os.getcwd()+"/model/")

downloadFromS3(BUCKET_NAME, KEY_1, 'AA_Trans_LSTM.json.data-00000-of-00002', os.getcwd()+"/model/06_06_Feb_05_2020/")
downloadFromS3(BUCKET_NAME, KEY_1, 'AA_Trans_LSTM.json.data-00001-of-00002', os.getcwd()+"/model/06_06_Feb_05_2020/")
downloadFromS3(BUCKET_NAME, KEY_1, 'AA_Trans_LSTM.json.index', os.getcwd()+"/model/06_06_Feb_05_2020/")
downloadFromS3(BUCKET_NAME, KEY_1, 'checkpoint', os.getcwd()+"/model/06_06_Feb_05_2020/")

downloadFromS3(BUCKET_NAME, KEY_2, 'AA_Trans_LSTM_Category.json.data-00000-of-00002', os.getcwd()+"/model/08_58_Feb_08_2020/")
downloadFromS3(BUCKET_NAME, KEY_2, 'AA_Trans_LSTM_Category.json.data-00001-of-00002', os.getcwd()+"/model/08_58_Feb_08_2020/")
downloadFromS3(BUCKET_NAME, KEY_2, 'AA_Trans_LSTM_Category.json.index', os.getcwd()+"/model/08_58_Feb_08_2020/")
downloadFromS3(BUCKET_NAME, KEY_2, 'checkpoint', os.getcwd()+"/model/08_58_Feb_08_2020/")


from BL_Category_Predict import BL_Category_Predict
from BL_VAD_Predict import BL_VAD_Predict

app = Flask(__name__, static_folder = "./dist/static", template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
category_predictor = BL_Category_Predict()
vad_predictor = BL_VAD_Predict()

@app.route('/api/random', methods=['GET'])
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/api/predict/category', methods=['POST'])
def predict_category():
    sentence = request.json['sentence']
    prediction = category_predictor.predict(sentence)
    response = {
        'category_1': prediction.tolist()[2],
        'category_2': prediction.tolist()[1],
        'category_3': prediction.tolist()[0]
    }
    return jsonify(response)

@app.route('/api/predict/vad', methods=['POST'])
def predict_vad():
    sentence = request.json['sentence']
    prediction = vad_predictor.predict(sentence)

    response = {
        'valence': str(prediction[0][0][0]),
        'arousal': str(prediction[1][0][0]),
        'dominance': str(prediction[2][0][0])
    }
    return jsonify(response)

@app.route('/api/predict', methods=['POST'])
def predict_all():
    sentence = request.json['sentence']
    print(sentence)
    cat_prediction = category_predictor.predict(sentence)
    vad_prediction = vad_predictor.predict(sentence)
    print(cat_prediction)
    print(vad_prediction)

    response = {
        'category_1': cat_prediction.tolist()[2],
        'category_2': cat_prediction.tolist()[1],
        'category_3': cat_prediction.tolist()[0],
        'valence': str(vad_prediction[0][0][0]),
        'arousal': str(vad_prediction[1][0][0]),
        'dominance': str(vad_prediction[2][0][0])
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:5000/{}'.format(path)).text
    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)




