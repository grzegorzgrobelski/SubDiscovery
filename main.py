
from flask import Flask, request
import mysql.connector
from config import DB_PASSWORD
from flask import jsonify

app = Flask(__name__)



def soql_connect():
    return mysql.connector.connect(
        host="mysql.mikr.us",
        user="yasmin464",
        password=DB_PASSWORD,
        database="db_yasmin464",
        port=3306
    )


def save_to_db_activitie(category, sub_category, value):
    conn = soql_connect()
    cursor = conn.cursor()

    query = """
    INSERT INTO activities (category, sub_category, value)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (category, sub_category, value))
    conn.commit()

    cursor.close()
    conn.close()



def save_to_db_wellbeing(mood, motivation, mindfulness, libido):
    conn = soql_connect()
    cursor = conn.cursor()

    query = """
    INSERT INTO wellbeing_metrics (mood, motivation, mindfulness, libido)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (mood, motivation, mindfulness, libido))
    conn.commit()

    cursor.close()
    conn.close()


@app.route("/activitie", methods=["POST"])
def post_activitie():

    print("==== REQUEST ====")

    data = request.get_json(silent=True)

    if data is None:
        data = request.form.to_dict()

    print("DATA:", data)

    category = data.get("category")
    sub_category = data.get("subCategory") 
    value = data.get("value")

    try:
        value = int(value) 
    except:
        return "Invalid value", 400

    save_to_db_activitie(category, sub_category, value)

    return {"status": "ok"}, 200


@app.route("/wellbeing", methods=["GET"])
def get_latest_wellbeing():

    conn = soql_connect()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM wellbeing_metrics
    ORDER BY created_at DESC
    LIMIT 1
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {"data": result}, 200

@app.route("/wellbeing", methods=["POST"])
def post_wellbeing():

    data = request.get_json(silent=True)

    # Garmin wysyła form-encoded
    if data is None:
        data = request.form.to_dict()

    print("DATA:", data)

    mood = data.get("mood")
    motivation = data.get("motivation")  # uwaga: Garmin camelCase!
    mindfulness = data.get("mindfulness")
    libido = data.get("libido")

    save_to_db_wellbeing(mood, motivation, mindfulness, libido)

    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
