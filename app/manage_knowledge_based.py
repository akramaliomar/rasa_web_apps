from flask import Flask, jsonify, redirect, url_for, render_template, request, session, flash, Blueprint
from .db_config import fetch_health, list_recommendations, save_recommendation, no_medicated_abnormalities
from .db_config import check_medication, check_abnormality, list_abnormalities, load_new_abnormalities_from_sensor
from .db_config import list_from_recommendations, fetch_abnormal_vs, list_from_medication, list_anomaly_recommendations1
from .db_config import save_new_recommendation, save_new_recommendation_list, save_new_recommendation_list_from_med
from .db_config import delete_medication
from datetime import timedelta
import json
import requests
import mysql.connector

manage_knowledge_based = Blueprint("manage_knowledge_based", __name__)


@manage_knowledge_based.route('/manage_knowledge_based', methods=['POST', 'GET'])
def manage_knowledge():
    if "username" in session:

        return render_template("manage_knowledge_based.html", status="yes",
                               content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0})
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/load_recommendations', methods=['POST', 'GET'])
def fetch_recommendations():
    if "username" in session:
        if request.method == "POST":
            recommendations = list_recommendations()
            return render_template("load_recommendations.html", recommendations=recommendations)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/load_abnormalities', methods=['POST', 'GET'])
def fetch_abnormalities():
    if "username" in session:
        if request.method == "POST":
            abnormalities = list_abnormalities()
            return render_template("load_abnormalities.html", abnormalities=abnormalities)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))

# @manage_knowledge_based.route('/load_abnormalities1', methods=['POST', 'GET'])
# def fetch_abnormalities1():
#     if request.method == "POST":
#         abnormalities = list_abnormalities()
#         return jsonify(abnormalities)
#         # return render_template("load_abnormalities.html", abnormalities=abnormalities)
#     else:
#         return "no data"
#

@manage_knowledge_based.route('/medication_panel', methods=['POST', 'GET'])
def provide_medications():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            # abnormalities = list_abnormalities()
            return render_template("medication_panel.html", diagnID=diagnID)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))

# @manage_knowledge_based.route('/from_recommendations_test', methods=['POST', 'GET'])
# def load_from_recommendations1():
#     if request.method == "POST":
#         diagnID = int(request.form["diagnID"])
#         context = "Any"
#         # return jsonify({"msg": str(diagnID)})
#         context = request.form["context"]
#         recommendations = list_from_recommendations(diagnID, context)
#         return jsonify(recommendations)
#         # return recommendations
#         # return fetch_abnormal_vs(diagnID)
#     else:
#         return jsonify({"msg": "no data"})
@manage_knowledge_based.route('/from_recommendations', methods=['POST', 'GET'])
def load_from_recommendations():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            context = "Any"
            # context = request.form["context"]
            recommendations = list_from_recommendations(diagnID, context)
            # return recommendations
            # return fetch_abnormal_vs(diagnID)
            return render_template("from_recommendations.html", recommendations=recommendations)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))




@manage_knowledge_based.route('/from_medication', methods=['POST', 'GET'])
def load_from_medication():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            context = request.form["context"]
            medications = list_from_medication(diagnID, context)
            # return medications
            # return fetch_abnormal_vs(diagnID)
            return render_template("from_medications.html", medications=medications)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/anomaly_recommendations', methods=['POST', 'GET'])
def load_anomaly_recommendations():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            recommendations = list_anomaly_recommendations1(diagnID)
            # return recommendations
            # return fetch_abnormal_vs(diagnID)
            return render_template("anomaly_recommendations.html", recommendations=recommendations)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/delete_medication', methods=['POST', 'GET'])
def delete_anomaly_recommendations():
    if "username" in session:
        if request.method == "POST":
            medID = int(request.form["medID"])
            delete = delete_medication(medID)
            return delete
        else:
            return "fail"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/new_recommendations', methods=['POST', 'GET'])
def new_recommnedation_form():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            context = request.form["context"]
            # medications = list_from_medication(diagnID, context)
            # return recommendations
            # return fetch_abnormal_vs(diagnID)
            health = fetch_health()
            return render_template("new_recommendation_form.html", diagnID=diagnID, health=health)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))


# @manage_knowledge_based.route('/load_abnormalities', methods=['POST', 'GET'])
# def fetch_abnormalities():
#     if request.method == "POST":
#         abnormalities = list_abnormalities()
#         return render_template("load_abnormalities.html", abnormalities=abnormalities)
#     else:
#         return "no data"


@manage_knowledge_based.route('/load_from_sensor', methods=['POST', 'GET'])
def generate_from_sensor():
    if "username" in session:
        total = load_new_abnormalities_from_sensor()
        if (total > 0):
            return str(total) + " record(s) added"
        else:
            return "No record added"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/load_reco_form', methods=['POST', 'GET'])
def recommendation_form():
    if "username" in session:
        if request.method == "POST":
            health = fetch_health()
            return render_template("recommendation_form.html", health=health)
        else:
            return "no data"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/save_reco_form', methods=['POST', 'GET'])
def save_recommendation_form():
    if "username" in session:
        if request.method == "POST":
            description = request.form["description"]
            reco_type = request.form["reco_type"]
            context = request.form["context"]
            health = json.loads(request.form["health"])
            status = save_recommendation(description, reco_type, context, health)
            return status
        else:
            return "no submission"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/save_new_reco_form', methods=['POST', 'GET'])
def save_anomaly_recommendation():
    if "username" in session:
        if request.method == "POST":
            description = request.form["description"]
            reco_type = request.form["reco_type"]
            context = request.form["context"]
            diagnID = request.form["diagnID"]
            # session.permanent = True
            username = session["username"]

            health = json.loads(request.form["health"])
            status = save_new_recommendation(description, reco_type, context, health, diagnID, username)
            return status
        else:
            return "no submission"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/update_medication', methods=['POST', 'GET'])
def save_anomaly_medication():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            # recolist = request.form["recolist"]
            recolist = json.loads(request.form["recolist"])
            username = session["username"]
            status = save_new_recommendation_list(diagnID, recolist, username)
            return status
        else:
            return "no submission"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/update_medication_from_med', methods=['POST', 'GET'])
def save_anomaly_medication_from_med():
    if "username" in session:
        if request.method == "POST":
            diagnID = request.form["diagnID"]
            # recolist = request.form["recolist"]
            diaglist = json.loads(request.form["diaglist"])
            username = session["username"]
            status = save_new_recommendation_list_from_med(diagnID, diaglist, username)
            return status
        else:
            return "no submission"
    else:
        return redirect(url_for("login"))


@manage_knowledge_based.route('/abnormalities', methods=['POST', 'GET'])
def none_medicated():
    return str(no_medicated_abnormalities())
