from flask import Flask, request, jsonify
from db_service import DbService
from fitatu_helper import FitatuHelper

app = Flask(__name__)


# -----------------------------
# ACTIVITIES
# -----------------------------
@app.route("/activitie", methods=["POST"])
def post_activitie():

    print("==== REQUEST ====")

    data = request.get_json(silent=True) or request.form.to_dict()

    print("DATA:", data)

    category = data.get("category")
    sub_category = data.get("subCategory")
    value = data.get("value")

    try:
        value = int(value)
    except:
        return {"error": "Invalid value"}, 400

    DbService.add_activity(category, sub_category, value)

    return {"status": "ok"}, 200

# -----------------------------
# WELLBEING
# -----------------------------
@app.route("/wellbeing", methods=["GET"])
def get_latest_wellbeing():

    result = DbService.get_latest_wellbeing()

    return {"data": result}, 200


@app.route("/wellbeing", methods=["POST"])
def post_wellbeing():

    data = request.get_json(silent=True) or request.form.to_dict()

    print("DATA:", data)

    mood = data.get("mood")
    motivation = data.get("motivation")
    mindfulness = data.get("mindfulness")
    libido = data.get("libido")

    DbService.add_wellbeing(mood, motivation, mindfulness, libido)

    return {"status": "ok"}, 200


# -----------------------------
# DAILY MACROS
# -----------------------------
@app.route("/daily_macros", methods=["GET"])
def get_daily_macros():
    try:
        macros = FitatuHelper.get_today_macros()
        return {"data": macros}, 200
    except Exception as e:
        return {"error": str(e)}, 500




# -----------------------------
# START APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)