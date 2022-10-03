import mysql.connector
from flask import jsonify
def open_connection():
    db = mysql.connector.connect(host='db_mysql_server', user='root', password='alsharif_2022', port=3306,
                                 database="vital_signs")
    return db


def db_get_vs():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM vital_sign_table  WHERE reload = 1 ORDER BY RAND ( ) LIMIT 1;')
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    get_vital_signs = jsonify(vital_signs)
                else:
                    get_vital_signs = jsonify([["0"]])
            return get_vital_signs
    except mysql.connector.Error as e:
        return jsonify([[str(e)]])

def db_get_reload_vs():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM vital_sign_table  WHERE reload = 1 ORDER BY RAND ( ) LIMIT 1;')
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    return vital_signs
                else:
                    get_vital_signs = [["0"]]
                return get_vital_signs
    except mysql.connector.Error as e:
        return [[str(e)]]


def reload_vs():
    try:
        conn = open_connection()
        with conn.cursor(dictionary=True) as cursor:
            result1 = cursor.execute('update vital_sign_table  set reload=0 WHERE reload=1;')
            result2 = cursor.execute('update vital_sign_table set reload=1 ORDER BY RAND() limit 1;')
        conn.commit()
        conn.close()
    except mysql.connector.Error as e:
        return [[str(e)]]

def db_aggregated_vs():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute(
                    "SELECT MAX(hr) as maxhr, MAX(spo2) AS maxspo2,MAX(resp) AS maxresp, MAX(tempr) as maxtempr, MIN(hr) as minhr, MIN(spo2) AS minspo2, MIN(resp) AS minresp, MIN(tempr) as mintempr, CONVERT(AVG(hr),CHAR) as avghr,CONVERT(AVG(spo2),CHAR) AS avgspo2, CONVERT(AVG(resp),CHAR) AS avgresp, CONVERT(AVG(tempr),CHAR) as avgtempr FROM vital_sign_table;")
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    get_vital_signs = jsonify(vital_signs)
                else:
                    get_vital_signs = jsonify([["0"]])
                return get_vital_signs
    except mysql.connector.Error as e:
        return jsonify([[str(e)]])

def db_get_rand_vs():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute("SELECT *  FROM vital_sign_table ORDER BY RAND ( ) LIMIT 1  ")
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    get_vital_signs = jsonify(vital_signs)
                else:
                    get_vital_signs = jsonify([["0"]])
                return get_vital_signs

                return get_vital_signs
    except mysql.connector.Error as e:
        return [[str(e)]]


def db_add_vs(v_signs):
    try:
        conn = open_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute('INSERT INTO vital_sign_table(timestamp, hr, spo2, resp, tempr) VALUES(%s, %s, %s, %s, %s)',
                           (v_signs["timestamp"], v_signs["hr"], v_signs["spo2"], v_signs["resp"], v_signs["tempr"]))
        conn.commit()
        conn.close()
    except mysql.connector.Error as e:
        return [[str(e)]]