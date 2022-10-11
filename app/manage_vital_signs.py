from flask import Flask, jsonify, redirect, url_for, render_template, request, session, flash, Blueprint
from .db_config import db_get_reload_vs, reload_vs, fetch_vital_signs, fetch_age_range, save_vital_signs
from datetime import timedelta
import json
import requests
import mysql.connector
import os


manage_vital_signs = Blueprint("manage_vital_signs", __name__)


@manage_vital_signs.route('/manage_vital_signs', methods=['POST', 'GET'])
def manage_vital_sign():
    os.system('mysqldump -u root -p%s vital_signs > database.sql' % 'alsharif_2022')
    return render_template("manage_vital_signs.html", status="yes",
                           content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0})
    # if "username" in session:
    #
    #     # vital_signs = db_get_reload_vs()
    #     #
    #     # if len(vital_signs[0]) > 1:
    #     #     return render_template("manage_vital_signs.html", status="yes",
    #     #                            content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
    #     #                                     "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"]})
    #     # else:
    #     #     return render_template("manage_vital_signs.html", status="yes",
    #     #                            content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0})
    #
    # return redirect(url_for("login"))

# @manage_vital_signs.route("/manage_vital_signs", methods=["POST", "GET"])  # this sets the route to this page
# def manage_vital_signs():
#     if "username" in session:
#         vital_signs = db_get_reload_vs()
#
#         if len(vital_signs[0]) > 1:
#             return render_template("manage_vital_signs.html", status="yes",
#                                    content={"temp": vital_signs[0]["tempr"], "resp": vital_signs[0]["resp"],
#                                             "spo2": vital_signs[0]["spo2"], "heart": vital_signs[0]["hr"]})
#         else:
#             return render_template("manage_vital_signs.html", status="yes",
#                                    content={"temp": 0, "resp": 0, "spo2": 0, "heart": 0})
#
#     return redirect(url_for("login"))


@manage_vital_signs.route('/vital_sign', methods=['POST', 'GET'])
def fetch_vital_sign():
    if request.method == "POST":
        tab = request.form["vital_signs"]
        vital_signs = fetch_vital_signs(tab)
        return render_template("vital_signs.html", tab=tab,  vital_signs=vital_signs)
    else:
        return "no data"

@manage_vital_signs.route('/load_vs_form', methods=['POST', 'GET'])
def vital_sign_form():
    if request.method == "POST":
        tab = request.form["tab"]
        age_range = fetch_age_range()
        return render_template("vital_sign_form.html", maxage=0, tab=tab, age_range=age_range)
    else:
        return "no data"

@manage_vital_signs.route('/save_vs_form', methods=['POST', 'GET'])
def save_vital_sign_form():
    if request.method == "POST":
        description = request.form["description"]
        minvalue = request.form["minvalue"]
        maxvalue = request.form["maxvalue"]
        age_range_name = request.form["age_range_name"]
        new_age_range = request.form["new_age_range"]
        min_age = request.form["min_age"]
        max_age = request.form["max_age"]
        tag = request.form["tag"]
        status = save_vital_signs(description, minvalue, maxvalue, age_range_name, new_age_range, min_age, max_age, tag)
        return status
    else:
        return "no submission"

