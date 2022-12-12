from flask import Flask, jsonify, redirect, url_for, render_template, request, session, flash, Blueprint
from .db_config import fetch_devices, save_device, get_device_logs, db_get_reload_vs, reload_vs, fetch_vital_signs, fetch_age_range, save_vital_signs
from datetime import timedelta
import json
import requests
import mysql.connector
import os

manage_device = Blueprint("manage_device", __name__)


@manage_device.route('/manage_device', methods=['POST', 'GET'])
def manage_devices():
    # os.system('mysqldump -u root -p%s vital_signs > database.sql' % 'alsharif_2022')
    return render_template("manage_devices.html")
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


@manage_device.route('/load_device_list', methods=['POST', 'GET'])
def fetch_device_list():
    if request.method == "POST":
        devices = fetch_devices()
        # return jsonify(devices)
        return render_template("device_lists.html", devices=devices)
    else:
        return "no data"


@manage_device.route('/load_device_logs', methods=['POST', 'GET'])
def fetch_device_logs():
    if request.method == "POST":
        device = fetch_devices()
        # deviceID = get_device(device[0]["device_no"])
        device_logs = get_device_logs(device[0]["deviceID"])
        # return jsonify(devices)
        return render_template("device_logs.html", device=device, device_logs=device_logs)
    else:
        return "no data"


@manage_device.route('/load_specific_device_logs', methods=['POST', 'GET'])
def fetch_specific_device_logs():
    if request.method == "POST":
        deviceID = int(request.form["deviceID"])
        device_logs = get_device_logs(deviceID)
        # return jsonify(devices)
        return render_template("device_specific_logs.html", device_logs=device_logs)
    else:
        return "no data"


@manage_device.route('/load_device_form', methods=['POST', 'GET'])
def device_form():
    if request.method == "POST":
        return render_template("device_form.html")
    else:
        return "no data"


@manage_device.route('/save_device_form', methods=['POST', 'GET'])
def save_new_device():
    if request.method == "POST":
        device_code = request.form["device_code"]
        device_no = request.form["device_no"]
        status = save_device(device_code, device_no)
        return status
    else:
        return "no submission"
