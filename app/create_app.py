from flask import Flask, jsonify, redirect, url_for, render_template, request, session, flash
from .db_config import db_get_reload_vs, reload_vs, check_user, get_device_data, get_device, read_recent_data_from_sensor
from .db_config import vital_signs_anomalies, get_device_list
from datetime import timedelta
from .api import api
from .manage_device import manage_device
from .manage_vital_signs import manage_vital_signs
from .manage_knowledge_based import manage_knowledge_based
import json
import requests
import mysql.connector
import tensorflow as tf
import numpy as np


def create_app():
    app = Flask(__name__)
    app.secret_key = "12345"
    app.permanent_session_lifetime = timedelta(minutes=10)
    app.register_blueprint(manage_vital_signs)
    app.register_blueprint(manage_knowledge_based)
    app.register_blueprint(manage_device)
    app.register_blueprint(api, url_prefix='/api')

    @app.route("/", methods=["POST", "GET"])  # this sets the route to this page
    @app.route("/login", methods=["POST", "GET"])  # this sets the route to this page
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            check = check_user(username, password)
            session.permanent = True
            if len(check) > 0:
                if check["user_status"] == 1:
                    session["username"] = check["userID"]
                    session["user_role"] = check["user_role"]
                    return redirect(url_for("dashboard"))
                else:
                    flash("The account has been blocked", "info")
                    return render_template("index.html")
            else:
                flash("Wrong username or password", "info")
                return render_template("index.html")
        else:
            if "username" in session:
                return redirect(url_for("dashboard"))

            return render_template("index.html")

    @app.route('/home', methods=['POST', 'GET'])
    def home():
        if request.method == 'GET':
            val = "hi"
            data = json.dumps({"sender": "Rasa", "message": val})
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            res = requests.post('http://154.53.40.198:80/webhooks/rest/webhook', data=data, headers=headers)
            res = res.json()
            val = res[0]['text']
            return render_template('home.html', val=val)

    @app.route('/predict', methods=['POST', 'GET'])
    def predict():
        testvalue = [[77., 93., 20., 26.]]
        loaded_model = tf.keras.models.load_model('./app/vital_signs.h5')  # loading the saved model
        predictions = loaded_model.predict(testvalue)  # making predictions
        vital_signs = int(np.argmax(predictions))  # index of maximum prediction
        probability = max(predictions.tolist()[0])  # probability of maximum prediction
        # print("Prediction: ", predictions.tolist())
        # print("Vital Sign: ", vital_signs)
        # print("Probability: ", probability)
        if vital_signs == 1:
            return "Abnormal"
        elif vital_signs == 0:
            return "Normal"

    # Defining the home page of our site
    @app.route("/dashboard")  # this sets the route to this page
    def dashboard():
        if "username" in session:
            # device_no = request.json['deviceNo']
            # device_no = "DVS0003"

            device = get_device_list()
            # deviceID = get_device(device[0]["device_no"])
            vital_signs = read_recent_data_from_sensor(device[0]["deviceID"])
            # vital_signs = db_get_reload_vs()

            if len(vital_signs[0]) > 0:
                anomalies = vital_signs_anomalies(vital_signs[0]["tempr"], vital_signs[0]["hr"], vital_signs[0]["resp"], vital_signs[0]["spo2"], "Normal", "Adult")
                if len(anomalies) > 0:
                    return render_template("dashboard.html", status="yes",device=device,
                                           content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
                                                    "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"], "btName": anomalies[0]["btName"], "respName": anomalies[0]["respName"],
                                                    "spName": anomalies[0]["spName"], "hrName": anomalies[0]["hrName"]})
                else:
                    return render_template("dashboard.html", status="yes",
                                           content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
                                                    "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"], "tempName": "", "respName": "",
                                                    "spName": "", "hrName": ""})


            # if len(vital_signs[0]) > 1:
            #     return render_template("dashboard.html", status="yes",
            #                            content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
            #                                     "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"]})
            else:
                return render_template("dashboard.html", status="yes",
                                       content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0,
                                                "tempName": "", "respName": "",
                                                "spName": "", "hrName": ""})
                # return render_template("dashboard.html", status="yes",
                #                        content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0})
        else:
            return redirect(url_for("login"))

    @app.route("/load_device_data", methods=['POST'])
    def get_recent_device_data():
        device_no = request.form['device_no']
        deviceID = get_device(device_no)
        device = get_device_list()

        vital_signs = read_recent_data_from_sensor(deviceID)
        # return " ".join(vital_signs)
        if len(vital_signs[0]) > 0:
            anomalies = vital_signs_anomalies(vital_signs[0]["tempr"], vital_signs[0]["hr"], vital_signs[0]["resp"],
                                              vital_signs[0]["spo2"], "Normal", "Adult")
            if len(anomalies) > 0:
                return render_template("current_vs.html", status="yes", device=device,
                                       content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
                                                "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"],
                                                "btName": anomalies[0]["btName"], "respName": anomalies[0]["respName"],
                                                "spName": anomalies[0]["spName"], "hrName": anomalies[0]["hrName"]})
            else:
                return render_template("current_vs.html", status="yes",
                                       content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
                                                "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"],
                                                "tempName": "", "respName": "",
                                                "spName": "", "hrName": ""})

        else:
            return render_template("current_vs.html", status="yes",
                                   content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0,
                                            "tempName": "", "respName": "",
                                            "spName": "", "hrName": ""})

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        flash("You have been logged out successfully", "info")
        return redirect(url_for("login"))

    @app.route("/reload")
    def reload():
        reload_vs()
        return redirect(url_for("dashboard", status="vs reloaded"))

    @app.route('/fetch_vs', methods=['GET'])
    def get_vital_signs():
        return db_get_vs()

    @app.route('/check', methods=['POST', 'GET'])
    def check():
        return render_template("webchat test2.html")

    @app.route('/mychat',methods=['POST'])
    def homechat():
        return render_template('chart.html')



    @app.route('/temp_xchart', methods=['POST'])
    def x_temp_chart():
        # device_no = request.form['deviceNo']
        device_no = request.json['deviceNo']
        # device_no = "DVS0003"
        deviceID = get_device(device_no)
        vital_signs = get_device_data(deviceID)
        data = []
        for row in vital_signs:
            data.append({'label': row['timestamp'], 'value': int(row['tempr'])})

        resp = jsonify(data)
        resp.status_code = 200
        return resp

    @app.route('/heart_xchart', methods=['POST'])
    def x_heart_chart():
        # device_no = request.form['deviceNo']
        device_no = request.json['deviceNo']
        # device_no = "DVS0003"
        deviceID = get_device(device_no)
        vital_signs = get_device_data(deviceID)
        data = []
        for row in vital_signs:
            data.append({'label': row['timestamp'], 'value': int(row['hr'])})

        resp = jsonify(data)
        resp.status_code = 200
        return resp

    @app.route('/resp_xchart', methods=['POST'])
    def x_resp_chart():
        # device_no = request.form['deviceNo']
        device_no = request.json['deviceNo']
        # device_no = "DVS0003"
        deviceID = get_device(device_no)
        vital_signs = get_device_data(deviceID)
        data = []
        for row in vital_signs:
            data.append({'label': row['timestamp'], 'value': int(row['resp'])})

        resp = jsonify(data)
        resp.status_code = 200
        return resp

    @app.route('/spo2_xchart', methods=['POST'])
    def x_spo2_chart():
        # device_no = request.form['deviceNo']
        device_no = request.json['deviceNo']
        # device_no = "DVS0003"
        deviceID = get_device(device_no)
        vital_signs = get_device_data(deviceID)
        data = []
        for row in vital_signs:
            data.append({'label': row['timestamp'], 'value': int(row['spo2'])})

        resp = jsonify(data)
        resp.status_code = 200
        return resp

    return app
