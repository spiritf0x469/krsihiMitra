from flask import Flask, request, jsonify
from flask_cors import CORS

from recommendation import recommend_crops, get_options

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "KrishiMitra backend is running"
    })


@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    state = data.get("state")
    season = data.get("season")
    area = data.get("area")
    rainfall = data.get("rainfall")

    if not state or not season or area is None or rainfall is None:
        return jsonify({
            "error": "please provide all required fields"
        }), 400

    try:
        area = float(area)
        rainfall = float(rainfall)
    except ValueError:
        return jsonify({
            "error": "area and rainfall must be numbers"
        }), 400

    recommendations = recommend_crops(
        state,
        season,
        area,
        rainfall
    )

    return jsonify({
        "recommendations": recommendations
    })

@app.route("/options", methods=["GET"])
def options():

    return jsonify(get_options())

if __name__ == "__main__":
    app.run(debug=True)