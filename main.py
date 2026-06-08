
from flask import Flask, request
import mysql.connector
from config import DB_PASSWORD

app = Flask(__name__)

def save_to_db(category, sub_category, value):
    conn = mysql.connector.connect(
        host="mysql.mikr.us",
        user="yasmin464",
        password=DB_PASSWORD,
        database="db_yasmin464",
        port=3306
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO activities (category, sub_category, value)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (category, sub_category, value))
    conn.commit()

    cursor.close()
    conn.close()


@app.route("/test", methods=["POST"])
def test():

    print("==== REQUEST ====")

    data = request.get_json(silent=True)

    # Garmin wysyła form-encoded
    if data is None:
        data = request.form.to_dict()

    print("DATA:", data)

    # ✅ pobieramy dane z requesta
    category = data.get("category")
    sub_category = data.get("subCategory")  # uwaga: Garmin camelCase!
    value = data.get("value")

    try:
        value = int(value)  # konwersja do int
    except:
        return "Invalid value", 400

    # ✅ zapis do bazy
    save_to_db(category, sub_category, value)

    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
