from flask import Flask, jsonify, request, Blueprint
from .db_config import db_add_vs, db_get_vs, db_aggregated_vs, db_get_rand_vs, read_data_from_sensor, save_data_from_sensor
from .db_config import read_recent_data_from_sensor, get_device, vital_signs_anomalies
from .db_config import add_new_abnormality, list_anomaly_recommendations, authenticate_device, fetch_abnormal_vs
import json
import requests
import mysql.connector
import tensorflow as tf
import numpy as np

api = Blueprint("api", __name__, url_prefix='/app')


# @api.route('/predict_anomaly', methods=['POST', 'GET'])
# def predict():
#
#     testvalue = [[77.5, 93.5, 20.5, 26.5]]
#     loaded_model = tf.keras.models.load_model('./app/vital_signs.h5')  # loading the saved model
#     predictions = loaded_model.predict(testvalue)  # making predictions
#     vital_signs = int(np.argmax(predictions))  # index of maximum prediction
#     probability = max(predictions.tolist()[0])  # probability of maximum prediction
#     # print("Prediction: ", predictions.tolist())
#     # print("Vital Sign: ", vital_signs)
#     # print("Probability: ", probability)
#     if vital_signs == 1:
#         return "Abnormal"
#     elif vital_signs == 0:
#         return "Normal"


@api.route('/predict_anomaly', methods=['POST', 'GET'])
def predict():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    deviceID = get_device(device_no)
    recent_data = read_recent_data_from_sensor(deviceID)
    if len(recent_data[0]) > 1:
        testvalue = [[float(recent_data[0]["hr"]), float(recent_data[0]["spo2"]), float(recent_data[0]["resp"]),
                      float(recent_data[0]["tempr"])]]
        loaded_model = tf.keras.models.load_model('./app/vital_signs.h5')  # loading the saved model
        predictions = loaded_model.predict(testvalue)  # making predictions
        vital_signs = int(np.argmax(predictions))  # index of maximum prediction
        probability = max(predictions.tolist()[0])  # probability of maximum prediction
        # print("Prediction: ", predictions.tolist())
        # print("Vital Sign: ", vital_signs)
        # print("Probability: ", probability)
        if vital_signs == 1:
            return jsonify("Abnormal")
        elif vital_signs == 0:
            return jsonify("Normal")
    else:
        return jsonify("No Data")


@api.route('/fetch_vs', methods=['POST', 'GET'])
def get_vital_signs():
    if not request.is_json:
        return jsonify([[{"tempr": "Unknown", "resp": "Unknown", "hr": "Unknown", "spo2": "Unknown"}],
                        [{"btName": "Unknown", "respName": "Unknown", "hrName": "Unknown", "spName": "Unknown"}]]), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    age = "Adult"
    # device_no = "DVS0003"
    deviceID = get_device(device_no)
    vital_signs = read_recent_data_from_sensor(deviceID)
    if len(vital_signs[0]) > 1:
        anomalies = vital_signs_anomalies(vital_signs[0]["tempr"], vital_signs[0]["hr"], vital_signs[0]["resp"],
                                          vital_signs[0]["spo2"], "Normal", age)
        agr = db_aggregated_vs(deviceID)
        if len(anomalies) > 0:

            readings  = [vital_signs, anomalies, agr]
            return jsonify(readings)
        else:
            return jsonify([vital_signs,
                            [{"btName": "Unknown", "respName": "Unknown", "hrName": "Unknown", "spName": "Unknown"}], agr])
    else:
        return jsonify([[{"tempr": "Unknown", "resp": "Unknown", "hr": "Unknown", "spo2": "Unknown"}],
                        [{"btName": "Unknown", "respName": "Unknown", "hrName": "Unknown", "spName": "Unknown"}], {"avgspo2": "Unknown", "avgtempr": "Unknown", "avghr": "Unknown", "avgresp": "Unknown", "avgtempr": "Unknown", "maxhr": "Unknown", "maxresp": "Unknown", "maxspo2": "Unknown", "maxtempr": "Unknown", "minhr": "Unknown", "minresp": "Unknown", "minspo2": "Unknown", "mintempr": "Unknown"}])


@api.route('/get_recommendtions_vs', methods=['POST', 'GET'])
def get_recommendations_vital_signs():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    age = json_data["age"]
    context = json_data["context"]
    health = json_data["health"]
    # device_no = "DVS0003"
    # age = "Adult"
    deviceID = get_device(device_no)
    # return jsonify(context)
    vital_signs = read_recent_data_from_sensor(deviceID)

    health = normalize_health_list(health)
    #return jsonify(health)
    # vs_ls = "\"Null\"," + ','.join(health)
    #return jsonify(vs_ls)
    # return jsonify(vital_signs)
    # vital_signs = db_get_reload_vs()
    if len(vital_signs[0]) > 0:
        anomalies = vital_signs_anomalies(vital_signs[0]["tempr"], vital_signs[0]["hr"], vital_signs[0]["resp"],
                                          vital_signs[0]["spo2"], "Normal", age)
        # return jsonify(anomalies)
        if len(anomalies) > 0:
            diagID = add_new_abnormality(anomalies[0]["hrID"], anomalies[0]["spID"], anomalies[0]["prID"], anomalies[0]["btID"], anomalies[0]["respID"])
            # vs_ls = "\"Null\"," + ','.join(fetch_abnormal_vs(diagID))
            # return jsonify(fetch_abnormal_vs(diagID))
            recommendations = list_anomaly_recommendations(diagID, context, health)
            return jsonify(recommendations)
            # recommendations = fetch_recommendations_for_anomalies(anomalies[0]["prID"], anomalies[0]["spID"],
            # anomalies[0]["hrID"], anomalies[0]["respID"], anomalies[0]["btID"])
        else:
            return jsonify([["no readings"]])
    return jsonify([["no readings"]])

#
# @api.route('/get_recommendtions_vs_test', methods=['POST', 'GET'])
# def get_recommendations_vital_signs_test():
#     if not request.is_json:
#         return jsonify({"msg": "Missing JSON in request"}), 400
#     json_data = request.get_json()
#     device_no = json_data["deviceNo"]
#     age = json_data["age"]
#     context = json_data["context"]
#     health = json_data["health"]
#     return jsonify({"sms": health[0]})

@api.route('/send_sensor_data', methods=['POST','GET'])
def send_sensor_data_vs():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    spo2 = float(json_data["spo2"])
    temp = float(json_data["temp"])
    heart = float(json_data["heart"])
    device_api_key = json_data["device_api_key"]
    deviceID = get_device(device_no)
    id  = save_data_from_sensor(deviceID, temp, 13, spo2, heart, 95)
    if id >=1:
        return jsonify({"msg": "success"}), 200
    else:
        return jsonify({"msg": "error"}), 200


@api.route('/authenticate_device_user', methods=['POST','GET'])
def authenticate_device_bot_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    device_key = str(json_data["device_key"])

    id = authenticate_device(device_no, device_key)
    return jsonify({"msg": str(id)}), 200


@api.route('/prediction', methods=['GET'])
def get_prediction_vs():
    return db_get_rand_vs()


@api.route('/add_vs', methods=['POST'])
def add_vital_signs():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    db_add_vs(request.get_json())
    return "Vital Signs added"


@api.route('/retrieve_recent_vs', methods=['POST'])
def recent_vital_signs():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    deviceID = get_device(device_no)
    sensor_data = read_data_from_sensor(deviceID)
    save = ""
    if len(sensor_data) > 0:
        save = save_data_from_sensor(deviceID, sensor_data["tempr"], sensor_data["resp"], sensor_data["spo2"],
                                     sensor_data["hr"], 95)

    recent_data = read_recent_data_from_sensor(deviceID)
    return jsonify(recent_data)

def normalize_health_list(health):
    health = list(map(lambda x: x.replace('hiv', 'HIV'), health))
    health = list(map(lambda x: x.replace('AIDS', 'HIV'), health))
    health = list(map(lambda x: x.replace('diabetics', 'Diabetics'), health))
    health = list(map(lambda x: x.replace('DIABETICS', 'Diabetics'), health))
    health = list(map(lambda x: x.replace('pregnant', 'Pregnant'), health))
    health = list(map(lambda x: x.replace('PREGNANT', 'Pregnant'), health))
    health = list(map(lambda x: x.replace('MALARIA', 'Malaria'), health))
    health = list(map(lambda x: x.replace('malaria', 'Malaria'), health))
    temp  = []
    result = [i for n, i in enumerate(health) if i not in health[:n]]
    result.append("Any")
    for i in result:
        temp.append("\"" + i + "\"")

    return temp