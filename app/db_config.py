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
                result = cursor.execute('SELECT *FROM sensor_data  WHERE reload = 1 ORDER BY RAND ( ) LIMIT 1;')
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    get_vital_signs = jsonify(vital_signs)
                else:
                    get_vital_signs = jsonify([["0"]])
            return get_vital_signs
    except mysql.connector.Error as e:
        return jsonify([[str(e)]])


def read_data_from_sensor(deviceID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM sensor_data  WHERE deviceID=%s ORDER BY RAND ( ) LIMIT 1;',
                                        (deviceID,))
                vital_signs = cursor.fetchall()
                for rows in vital_signs:
                    return rows
                else:
                    return []
    except mysql.connector.Error as e:
        return []


def get_device(deviceNo):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM device_subscription  WHERE device_no=%s LIMIT 1;',
                                        (deviceNo,))
                device = cursor.fetchall()
                for row in device:
                    return row["deviceID"]
                return 0
    except mysql.connector.Error as e:
        return 0


def get_device_list():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM device_subscription WHERE deviceID IN(SELECT DISTINCT(deviceID) '
                                        'from vital_signs) ORDER BY device_no;')
                device = cursor.fetchall()
                if len(device)>0:
                    return device
                return [[""]]
    except mysql.connector.Error as e:
        return [[""]]


def read_recent_data_from_sensor(deviceID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM vital_signs  WHERE deviceID=%s ORDER BY vital_sign_id DESC '
                                        'LIMIT 1;',
                                        (deviceID,))
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    get_vital_signs = vital_signs
                else:
                    get_vital_signs = [["0"]]
                return get_vital_signs
    except mysql.connector.Error as e:
        return [[str(e)]]


def save_data_from_sensor(deviceID, tempr, resp, spo2, hr, pr):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute(
                    'INSERT INTO vital_signs(deviceID, hr, spo2, resp, tempr, pressure) VALUES(%s, %s, %s, %s, %s, %s)',
                    (deviceID, hr, spo2, resp, tempr, pr))
                conn.commit()
                vital_signs_id = cursor.lastrowid
                return str(vital_signs_id)

    except mysql.connector.Error as e:
        return str(e)


def check_user(userID, password):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM users  WHERE userID=%s AND user_password=%s;', (userID, password))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    for row in rows:
                        return row
                else:
                    return []
                return []
    except mysql.connector.Error as e:
        return []


def get_device_data(deviceID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM vital_signs  WHERE deviceID=%s ORDER BY timestamp DESC ;',
                                        (deviceID,))
                rows = cursor.fetchall()
                if len(rows):
                    return rows
                return [[]]

    except mysql.connector.Error as e:
        return [[]]


def fetch_vital_signs(vital_sign):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                if vital_sign == "heart rate":
                    result = cursor.execute(
                        'SELECT *FROM patient_age_range INNER JOIN heart_rate USING(ageID) ORDER BY minage ASC, hrmin ASC;')

                elif vital_sign == "temperature":
                    result = cursor.execute(
                        'SELECT *FROM patient_age_range INNER JOIN body_temperature USING(ageID) ORDER BY minage ASC, btmin ASC;')

                elif vital_sign == "spo2":
                    result = cursor.execute(
                        'SELECT *FROM patient_age_range INNER JOIN spo2 USING(ageID) ORDER BY minage ASC, minsp ASC;')

                elif vital_sign == "respiration":
                    result = cursor.execute(
                        'SELECT *FROM patient_age_range INNER JOIN respiration USING(ageID) ORDER BY minage ASC, minresp ASC;')

                elif vital_sign == "pressure":
                    result = cursor.execute(
                        'SELECT *FROM patient_age_range INNER JOIN pressure USING(ageID) ORDER BY minage ASC, minpr ASC;')

                else:
                    result = cursor.execute(
                        'SELECT *FROM patient_age_range INNER JOIN body_temperature USING(ageID) ORDER BY minage ASC, btmin ASC;')

                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    return vital_signs
                else:
                    get_vital_signs = []
                return get_vital_signs
    except mysql.connector.Error as e:
        return []


def list_recommendations():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute(
                    'SELECT *FROM recommendations ORDER BY recoDescription ASC, recoType ASC;')

                rows = cursor.fetchall()
                if len(rows) > 0:
                    return rows
                else:
                    rows = []
                return rows
    except mysql.connector.Error as e:
        return []


def fetch_health():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM patient_health ORDER BY description ASC;')
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return rows
                else:
                    rows = []
                return rows
    except mysql.connector.Error as e:
        return []


def fetch_age_range():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM patient_age_range ORDER BY minage ASC')
                age_ranges = cursor.fetchall()
                if len(age_ranges) > 0:
                    return age_ranges
                else:
                    get_age_range = []
                return get_vital_range
    except mysql.connector.Error as e:
        return []


def fetch_abnormal_vs(diagID):
    vs_ls = []
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT hrName as Breathing, respName as Respiration, spName as Spo2, '
                                        ' btName as Temperature, prName as Pressure '
                                        'FROM (((((patient_age_range INNER JOIN heart_rate USING(ageID)) INNER JOIN '
                                        'spo2 USING(ageID)) INNER JOIN respiration USING(ageID)) '
                                        'INNER JOIN pressure USING(ageID)) INNER JOIN body_temperature USING(ageID)) '
                                        'INNER JOIN symptomes_abmonality ON CONCAT(heart_rate.hrID,"-",spo2.spID,"-",'
                                        'pressure.prID,"-",respiration.respID,"-",body_temperature.btID)=CONCAT('
                                        'symptomes_abmonality.hrID,"-",symptomes_abmonality.spID,"-",'
                                        'symptomes_abmonality.prID,"-",symptomes_abmonality.respID,"-",'
                                        'symptomes_abmonality.btID) WHERE diagnosisID=%s;', (diagID,))
                rows = cursor.fetchall()
                # return str(len(rows))+"DID - "+str(diagID)
                for vs in rows:
                    vs_ls = find_keys_by_values(vs, "Normal")
                return vs_ls
    except mysql.connector.Error as e:
        return []


def find_keys_by_values(dict, val_to_find):
    # listofvalues = dict.items()
    listofkeys = list()
    for key, value in dict.items():
        if value != val_to_find:
            listofkeys.append("\"" + key + "\"")
    return listofkeys


def list_from_recommendations(diagnID, context):
    try:
        conn = open_connection()
        with conn:
            vs_ls = "\"Null\"," + ','.join(fetch_abnormal_vs(diagnID))
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM recommendations WHERE recoType IN (' + vs_ls + ') AND recoID NOT '
                                                                                                     'IN(SELECT recoID '
                                                                                                     'FROM medications '
                                                                                                     'WHERE '
                                                                                                     'diagnosisID=%s)',
                                        (diagnID,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return rows
                else:
                    rows = []
                return rows
    except mysql.connector.Error as e:
        return []


def list_anomaly_recommendations(diagnID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM recommendations INNER JOIN medications USING(recoID) WHERE '
                                        'diagnosisID=%s ORDER BY sequenceNo ASC,recoType ASC', (diagnID,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return rows
                else:
                    rows = [[]]
                return rows
    except mysql.connector.Error as e:
        return [[]]


def list_from_medication(diagnID, context):
    try:
        conn = open_connection()
        with conn:
            vs_ls = "\"Null\"," + ','.join(fetch_abnormal_vs(diagnID))

            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT ageName, minage, maxage, hrName, hrmax, hrmin, respName, minresp, '
                                        'maxresp, spName, minsp, maxsp, btName, btmax, btmin, prName, minpr, maxpr, '
                                        'status, diagnosisID FROM (((((patient_age_range INNER JOIN heart_rate USING('
                                        'ageID)) INNER JOIN spo2 USING(ageID)) INNER JOIN respiration USING(ageID)) '
                                        'INNER JOIN pressure USING(ageID)) INNER JOIN body_temperature USING(ageID)) '
                                        'INNER JOIN symptomes_abmonality ON CONCAT(heart_rate.hrID,"-",spo2.spID,"-",'
                                        'pressure.prID,"-",respiration.respID,"-",body_temperature.btID)=CONCAT('
                                        'symptomes_abmonality.hrID,"-",symptomes_abmonality.spID,"-",'
                                        'symptomes_abmonality.prID,"-",symptomes_abmonality.respID,"-",'
                                        'symptomes_abmonality.btID) WHERE symptomes_abmonality.diagnosisID IN(SELECT '
                                        'DISTINCT(diagnosisID) AS diagID FROM recommendations INNER JOIN medications '
                                        'USING(recoID) WHERE recoType IN (' + vs_ls + '))')
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return rows
                else:
                    rows = [[]]
                return rows
    except mysql.connector.Error as e:
        return [[]]


def list_abnormalities():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT ageName, minage, maxage, hrName, hrmax, hrmin, respName, minresp, '
                                        'maxresp, spName, minsp, maxsp, btName, btmax, btmin, prName, minpr, maxpr, '
                                        'status, diagnosisID FROM (((((patient_age_range INNER JOIN heart_rate USING('
                                        'ageID)) INNER JOIN spo2 USING(ageID)) INNER JOIN respiration USING(ageID)) '
                                        'INNER JOIN pressure USING(ageID)) INNER JOIN body_temperature USING(ageID)) '
                                        'INNER JOIN symptomes_abmonality ON CONCAT(heart_rate.hrID,"-",spo2.spID,"-",'
                                        'pressure.prID,"-",respiration.respID,"-",body_temperature.btID)=CONCAT('
                                        'symptomes_abmonality.hrID,"-",symptomes_abmonality.spID,"-",'
                                        'symptomes_abmonality.prID,"-",symptomes_abmonality.respID,"-",'
                                        'symptomes_abmonality.btID) ORDER BY symptomes_abmonality.status ASC;')
                abnormalities = cursor.fetchall()
                if len(abnormalities) > 0:
                    return abnormalities
                else:
                    return []
    except mysql.connector.Error as e:
        return []


def save_vital_signs(description, minvalue, maxvalue, age_range_name, new_age_range, min_age, max_age, tag):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:

                if age_range_name == "new":
                    check = cursor.execute('SELECT *FROM patient_age_range WHERE ageName=%s', (new_age_range,))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return "exist"
                    else:
                        result = cursor.execute(
                            'INSERT INTO patient_age_range(ageName, minage, maxage) VALUES(%s, %s, %s)',
                            (new_age_range, min_age, max_age))
                        conn.commit()
                        age_range_name = cursor.lastrowid

                if tag == "heart rate":
                    check1 = cursor.execute('SELECT *FROM heart_rate WHERE hrName=%s AND ageID=%s',
                                            (description, age_range_name))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return "v-exist"
                    else:
                        result = cursor.execute(
                            'INSERT INTO heart_rate(hrName, hrmin, hrmax, ageID) VALUES(%s, %s, %s, %s)',
                            (description, minvalue, maxvalue, age_range_name))
                        conn.commit()
                        return "success"


                elif tag == "temperature":
                    check1 = cursor.execute('SELECT *FROM body_temperature WHERE btName=%s AND ageID=%s',
                                            (description, age_range_name))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return "v-exist"
                    else:
                        result = cursor.execute(
                            'INSERT INTO body_temperature(btName, btmin, btmax, ageID) VALUES(%s, %s, %s, %s)',
                            (description, minvalue, maxvalue, age_range_name))
                        conn.commit()
                        return "success"


                elif tag == "spo2":
                    check1 = cursor.execute('SELECT *FROM spo2 WHERE spName=%s AND ageID=%s',
                                            (description, age_range_name))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return "v-exist"
                    else:
                        result = cursor.execute(
                            'INSERT INTO spo2(spName, minsp, maxsp, ageID) VALUES(%s, %s, %s, %s)',
                            (description, minvalue, maxvalue, age_range_name))
                        conn.commit()
                        return "success"


                elif tag == "respiration":
                    check1 = cursor.execute('SELECT *FROM respiration WHERE respName=%s AND ageID=%s',
                                            (description, age_range_name))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return "v-exist"
                    else:
                        result = cursor.execute(
                            'INSERT INTO respiration(respName, minresp, maxresp, ageID) VALUES(%s, %s, %s, %s)',
                            (description, minvalue, maxvalue, age_range_name))
                        conn.commit()
                        return "success"

                elif tag == "pressure":
                    check1 = cursor.execute('SELECT *FROM pressure WHERE prName=%s AND ageID=%s',
                                            (description, age_range_name))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return "v-exist"
                    else:
                        result = cursor.execute(
                            'INSERT INTO pressure(prName, minpr, maxpr, ageID) VALUES(%s, %s, %s, %s)',
                            (description, minvalue, maxvalue, age_range_name))
                        conn.commit()
                        return "success"
    except mysql.connector.Error as e:
        return jsonify([str(e)])


def save_recommendation(description, reco_type, context, health):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                check = cursor.execute('SELECT *FROM recommendations WHERE recoDescription=%s', (description,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return "exist"
                else:
                    result = cursor.execute(
                        'INSERT INTO recommendations(recoDescription, recoType, context) VALUES(%s, %s, %s)',
                        (description, reco_type, context))
                    conn.commit()
                    recoID = cursor.lastrowid
                    for healthID in health:
                        result = cursor.execute(
                            'INSERT INTO exception_deseases(healthID, recoID) VALUES(%s, %s)',
                            (healthID, recoID))
                        conn.commit()
                    return "success"

    except mysql.connector.Error as e:
        return str(e)


def save_new_recommendation(description, reco_type, context, health, diagnID, userID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                check = cursor.execute('SELECT *FROM recommendations WHERE recoDescription=%s', (description,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return "exist"
                else:
                    result = cursor.execute(
                        'INSERT INTO recommendations(recoDescription, recoType, context) VALUES(%s, %s, %s)',
                        (description, reco_type, context))
                    conn.commit()
                    recoID = cursor.lastrowid
                    for healthID in health:
                        result = cursor.execute(
                            'INSERT INTO exception_deseases(healthID, recoID) VALUES(%s, %s)',
                            (healthID, recoID))
                        conn.commit()
                    check = cursor.execute(
                        'SELECT IFNULL(MAX(sequenceNo),0) as maxno FROM medications WHERE diagnosisID=%s', (diagnID,))
                    rows = cursor.fetchall()
                    sequenceNo = 0;
                    for row in rows:
                        sequenceNo = row["maxno"] + 1
                    result = cursor.execute(
                        'INSERT INTO medications(diagnosisID, recoID, userID, sequenceNo) VALUES(%s, %s, %s, %s)',
                        (diagnID, recoID, userID, sequenceNo))
                    conn.commit()
                    return "success"
    except mysql.connector.Error as e:
        return str(e)


def save_new_recommendation(description, reco_type, context, health, diagnID, userID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                check = cursor.execute('SELECT *FROM recommendations WHERE recoDescription=%s', (description,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return "exist"
                else:
                    result = cursor.execute(
                        'INSERT INTO recommendations(recoDescription, recoType, context) VALUES(%s, %s, %s)',
                        (description, reco_type, context))
                    conn.commit()
                    recoID = cursor.lastrowid
                    for healthID in health:
                        result = cursor.execute(
                            'INSERT INTO exception_deseases(healthID, recoID) VALUES(%s, %s)',
                            (healthID, recoID))
                        conn.commit()
                    check = cursor.execute(
                        'SELECT IFNULL(MAX(sequenceNo),0) as maxno FROM medications WHERE diagnosisID=%s', (diagnID,))
                    rows = cursor.fetchall()
                    sequenceNo = 0;
                    for row in rows:
                        sequenceNo = row["maxno"] + 1
                    result = cursor.execute(
                        'INSERT INTO medications(diagnosisID, recoID, userID, sequenceNo) VALUES(%s, %s, %s, %s)',
                        (diagnID, recoID, userID, sequenceNo))
                    conn.commit()
                    return "success"
    except mysql.connector.Error as e:
        return str(e)


def save_new_recommendation_list(diagnID, recolist, userID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                check = cursor.execute(
                    'SELECT IFNULL(MAX(sequenceNo),0) as maxno FROM medications WHERE diagnosisID=%s', (diagnID,))
                rows = cursor.fetchall()
                sequenceNo = 0;
                for row in rows:
                    sequenceNo = row["maxno"] + 1

                for recoID in recolist:
                    recoID = int(recoID)
                    check = cursor.execute('SELECT * from medications WHERE diagnosisID=%s AND recoID=%s',
                                           (diagnID, recoID))
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        continue
                    result = cursor.execute(
                        'INSERT INTO medications(diagnosisID, recoID, userID, sequenceNo) VALUES(%s, %s, %s, %s)',
                        (diagnID, recoID, userID, sequenceNo))
                    conn.commit()
                return "success"
    except mysql.connector.Error as e:
        return ",".join(recolist)


def save_new_recommendation_list_from_med(diagnID, diaglist, userID):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                check = cursor.execute(
                    'SELECT IFNULL(MAX(sequenceNo),0) as maxno FROM medications WHERE diagnosisID=%s', (diagnID,))
                rows = cursor.fetchall()
                sequenceNo = 0;
                for row in rows:
                    sequenceNo = row["maxno"] + 1

                for diagID in diaglist:
                    diagID = int(diagID)
                    check = cursor.execute('SELECT * from medications WHERE diagnosisID=%s',
                                           (diagID,))
                    rows = cursor.fetchall()
                    for row in rows:
                        recoID = row["recoID"]
                        check = cursor.execute('SELECT * from medications WHERE diagnosisID=%s AND recoID=%s',
                                                   (diagnID, recoID))
                        rows1 = cursor.fetchall()
                        if len(rows1) > 0:
                            continue
                        result = cursor.execute(
                                'INSERT INTO medications(diagnosisID, recoID, userID, sequenceNo) VALUES(%s, %s, %s, '
                                '%s)',
                                (diagnID, recoID, userID, sequenceNo))
                        conn.commit()
                return "success"

    except mysql.connector.Error as e:
        return str(e)


def db_get_reload_vs():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *FROM sensor_data  WHERE reload = 1 ORDER BY RAND ( ) LIMIT 1;')
                vital_signs = cursor.fetchall()
                if len(vital_signs) > 0:
                    return vital_signs
                else:
                    get_vital_signs = [["0"]]
                return get_vital_signs
    except mysql.connector.Error as e:
        return str(e)


def reload_vs():
    try:
        conn = open_connection()
        with conn.cursor(dictionary=True) as cursor:
            result1 = cursor.execute('update sensor_data  set reload=0 WHERE reload=1;')
            result2 = cursor.execute('update sensor_data set reload=1 ORDER BY RAND() limit 1;')
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
                    "SELECT MAX(hr) as maxhr, MAX(spo2) AS maxspo2,MAX(resp) AS maxresp, MAX(tempr) as maxtempr, MIN(hr) as minhr, MIN(spo2) AS minspo2, MIN(resp) AS minresp, MIN(tempr) as mintempr, CONVERT(AVG(hr),CHAR) as avghr,CONVERT(AVG(spo2),CHAR) AS avgspo2, CONVERT(AVG(resp),CHAR) AS avgresp, CONVERT(AVG(tempr),CHAR) as avgtempr FROM sensor_data;")
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
                result = cursor.execute("SELECT *  FROM sensor_data ORDER BY RAND ( ) LIMIT 1  ")
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
            cursor.execute('INSERT INTO sensor_data(timestamp, hr, spo2, resp, tempr) VALUES(%s, %s, %s, %s, %s)',
                           (v_signs["timestamp"], v_signs["hr"], v_signs["spo2"], v_signs["resp"], v_signs["tempr"]))
        conn.commit()
        conn.close()
    except mysql.connector.Error as e:
        return [[str(e)]]


def check_abnormality(heart, spo2, pressure, temperature, respiration):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT diagnosisID FROM symptomes_abmonality WHERE hrID=%s AND spID=%s AND '
                                        'prID=%s AND '
                                        'respID=%s AND btID=%s', (heart, spo2, pressure, respiration, temperature))
                rows = cursor.fetchone()
                if len(rows) > 0:
                    return rows["diagnosisID"]
                else:
                    cursor.execute(
                        'INSERT INTO symptomes_abmonality(hrID, spID, prID, respID, btID) VALUES(%s, %s, %s, %s, %s)',
                        (heart, spo2, pressure, respiration, temperature))
                    conn.commit()
                    return cursor.lastrowid
    except mysql.connector.Error as e:
        return 0


def add_abnormality(heart, spo2, pressure, temperature, respiration):
    count = 0
    conn = open_connection()
    try:
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT diagnosisID FROM symptomes_abmonality WHERE hrID=%s AND spID=%s AND '
                                        'prID=%s AND '
                                        'respID=%s AND btID=%s', (heart, spo2, pressure, respiration, temperature))
                rows = cursor.fetchall()
                if len(rows) == 0:
                    cursor.execute(
                        'INSERT INTO symptomes_abmonality(hrID, spID, prID, respID, btID) VALUES(%s, %s, %s, %s, %s)',
                        (heart, spo2, pressure, respiration, temperature))
                    conn.commit()
                    count += 1
            conn.close()
            return count
    except mysql.connector.Error as e:
        return count


def add_new_abnormality(heart, spo2, pressure, temperature, respiration):
    diagnosisID = 0
    conn = open_connection()
    try:
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT diagnosisID FROM symptomes_abmonality WHERE hrID=%s AND spID=%s AND '
                                        'prID=%s AND '
                                        'respID=%s AND btID=%s', (heart, spo2, pressure, respiration, temperature))
                rows = cursor.fetchall()
                if len(rows) == 0:
                    cursor.execute(
                        'INSERT INTO symptomes_abmonality(hrID, spID, prID, respID, btID) VALUES(%s, %s, %s, %s, %s)',
                        (heart, spo2, pressure, respiration, temperature))
                    conn.commit()
                    diagnosisID = cursor.lastrowid
                else:
                    diagnosisID = rows[0]["diagnosisID"]
            conn.close()
            return diagnosisID
    except mysql.connector.Error as e:
        return 0


def check_medication(diagnosis):
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT medID FROM medication WHERE diagnosisID=%s', (diagnosis,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    return True
                else:
                    return False
    except mysql.connector.Error as e:
        return 0


def no_medicated_abnormalities():
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT COUNT(*) AS total FROM symptomes_abmonality WHERE diagnosisID NOT IN('
                                        'SELECT diagnosisID FROM medications)')
                rows = cursor.fetchone()
                return rows["total"]
    except mysql.connector.Error as e:
        return 0


def load_new_abnormalities_from_sensor(age="Adult"):
    added = 0;
    try:
        conn = open_connection()
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute('SELECT *  FROM sensor_data ORDER BY RAND ( ) LIMIT 5 ')
                sensor_data = cursor.fetchall()
                for row in sensor_data:
                    vs_ab = vital_signs_anomalies(row["tempr"], row["hr"], row["resp"], row["spo2"], "Normal", age)
                    # s = s + " heart: " + str(row["hr"])+" tempr: " + str(row["tempr"])+" resp: " + str(row["resp"])+" spo2: " + str(row["spo2"])+"len(vs_ab): "+vs_ab+"===>"
                    if len(vs_ab) > 0:
                        # vb = vb + "=>heart: " + str(vs_ab["hrID"])
                        for vs in vs_ab:
                            added += add_abnormality(vs["hrID"], vs["spID"], vs["prID"], vs["btID"], vs["respID"])
        conn.close()
        return added
    except mysql.connector.Error as e:
        return added


def vital_signs_anomalies(temp=-1, hr=-1, resp=-1, sp=-1, pr=-1, age=-1):
    if isinstance(age, str):
        ageName = age
    else:
        ageName = ""
        if isinstance(age, int) and (age < 0 or age > 150):
            ageName = "Adult"

    if temp < 0:
        tempName = "Normal"
    else:
        tempName = ""
    if hr < 0:
        hrName = "Normal"
    else:
        hrName = ""

    if resp < 0:
        respName = "Normal"
    else:
        respName = ""

    if sp < 0:
        spName = "Normal"
    else:
        spName = ""

    if isinstance(pr, int) and (age < 0 or age > 150):
        if pr < 0:
            prName = "Normal"
        else:
            prName = ""
    else:
        prName = "Normal"
        pr = -1
    conn = open_connection()
    try:
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                result = cursor.execute(
                    'SELECT prID, prName, spID, spName,  hrID, hrName, respID, respName, btID, btName FROM (((('
                    'patient_age_range INNER JOIN heart_rate USING( '
                    'ageID)) INNER JOIN spo2 USING(ageID)) INNER JOIN respiration USING(ageID)) INNER JOIN pressure '
                    'USING(ageID)) INNER JOIN body_temperature USING(ageID) WHERE (ageName=%s OR (minage<=%s AND '
                    'maxage>=%s)) AND (hrName=%s OR (hrmin<=%s AND hrmax>=%s)) AND (respName=%s OR (minresp<=%s AND '
                    'maxresp>=%s)) AND (spName=%s OR (minsp<=%s AND maxsp>=%s)) AND (prName=%s OR (minpr<=%s AND '
                    'maxpr>=%s)) AND (btName=%s OR (btmin<=%s AND btmax>=%s))',
                    (ageName, age, age, hrName, hr, hr, respName, resp, resp, spName, sp, sp, prName, pr, pr, tempName,
                     temp, temp))
                sensor_data = cursor.fetchall()
                if len(sensor_data) > 0:
                    return sensor_data
                else:
                    return []
            conn.close()
    except mysql.connector.Error as e:
        return []
