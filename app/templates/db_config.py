from flask import Flask, jsonify, redirect, url_for, render_template, request, session, flash
from db import db_add_vs, db_get_vs, db_aggregated_vs, db_get_rand_vs, db_get_reload_vs, reload_vs
from datetime import timedelta
import json
import requests
import mysql.connector
from db import db_add_vs, db_get_vs, db_aggregated_vs, db_get_rand_vs, db_get_reload_vs, reload_vs


def create_app():
    app = Flask(__name__)
    app.secret_key = "12345"
    app.permanent_session_lifetime = timedelta(minutes=5)

    @app.route("/", methods=["POST", "GET"])  # this sets the route to this page
    @app.route("/login", methods=["POST", "GET"])  # this sets the route to this page
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            session.permanent = True
            session["username"] = username
            return redirect(url_for("dashboard"))
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


    # Defining the home page of our site
    @app.route("/dashboard")  # this sets the route to this page
    def dashboard():
        if "username" in session:
            vital_signs = db_get_reload_vs()

            if len(vital_signs[0]) > 1:
                return render_template("dashboard.html", status="yes",
                                       content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
                                                "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"]})
            else:
                return render_template("dashboard.html", status="yes",
                                       content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0})
        else:
            return redirect(url_for("login"))


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


    @app.route('/test', methods=['POST', 'GET'])
    def test():
        return render_template("test.html")


    @app.route('/fetch_aggr_vs', methods=['GET'])
    def get_aggregated_vs():
        return db_aggregated_vs()


    @app.route('/prediction', methods=['GET'])
    def get_prediction_vs():
        # testvalue = [[77., 93., 20., 26.]]
        #
        # loaded_model = tf.keras.models.load_model('vital_signs.h5')  # loading the saved model
        # predictions = loaded_model.predict(testvalue)  # making predictions
        # vital_signs = int(np.argmax(predictions))  # index of maximum prediction
        # probability = max(predictions.tolist()[0])  # probability of maximum prediction
        # # print("Prediction: ", predictions.tolist())
        # # print("Vital Sign: ", vital_signs)
        # # print("Probability: ", probability)
        return db_get_rand_vs()


    @app.route('/add_vs', methods=['POST'])
    def add_vital_signs():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        db_add_vs(request.get_json())
        return "Vital Signs added"
    
    return app