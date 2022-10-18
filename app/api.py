from flask import Flask, jsonify, request, Blueprint
from .db_config import db_add_vs, db_get_vs, db_aggregated_vs, db_get_rand_vs, read_data_from_sensor, save_data_from_sensor
from .db_config import read_recent_data_from_sensor, get_device, vital_signs_anomalies, add_new_abnormality, list_anomaly_recommendations
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
        if len(anomalies) > 0:
            readings  = [vital_signs, anomalies]
            return jsonify(readings)
        else:
            return jsonify([vital_signs,
                            [{"btName": "Unknown", "respName": "Unknown", "hrName": "Unknown", "spName": "Unknown"}]])
    else:
        return jsonify([[{"tempr": "Unknown", "resp": "Unknown", "hr": "Unknown", "spo2": "Unknown"}],
                        [{"btName": "Unknown", "respName": "Unknown", "hrName": "Unknown", "spName": "Unknown"}]])


@api.route('/get_recommendtions_vs', methods=['POST', 'GET'])
def get_recommendations_vital_signs():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    json_data = request.get_json()
    device_no = json_data["deviceNo"]
    # device_no = "DVS0003"
    age = "Adult"
    deviceID = get_device(device_no)
    vital_signs = read_recent_data_from_sensor(deviceID)
    # return jsonify(vital_signs)
    # vital_signs = db_get_reload_vs()
    if len(vital_signs[0]) > 0:
        anomalies = vital_signs_anomalies(vital_signs[0]["tempr"], vital_signs[0]["hr"], vital_signs[0]["resp"],
                                          vital_signs[0]["spo2"], "Normal", age)
        # return jsonify(anomalies)
        if len(anomalies) > 0:
            diagID = add_new_abnormality(anomalies[0]["hrID"], anomalies[0]["spID"], anomalies[0]["prID"], anomalies[0]["btID"], anomalies[0]["respID"])
            recommendations = list_anomaly_recommendations(diagID)
            return jsonify(recommendations)
            # recommendations = fetch_recommendations_for_anomalies(anomalies[0]["prID"], anomalies[0]["spID"],
            # anomalies[0]["hrID"], anomalies[0]["respID"], anomalies[0]["btID"])
        else:
            return jsonify([["no readings"]])
    return jsonify([["no readings"]])


@api.route('/fetch_aggr_vs', methods=['GET'])
def get_aggregated_vs():
    return db_aggregated_vs()


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