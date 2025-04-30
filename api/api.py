from flask import Flask, request, jsonify
from locations import add_location, get_nearby, get_distance, get_all_places, save_user_location, get_distance_between_user_and_place
from flask_cors import CORS
# import redis

app = Flask(__name__)
# CORS(app)
CORS(app, origins=["http://localhost:*"], allow_headers=["Content-Type","Access-Control-Allow-Origin"], methods=["GET", "POST", "PUT"])


@app.route("/add", methods=["POST"])
def add():
    data = request.json
    try:
        add_location(data["group"], data["name"], data["lon"], data["lat"])
        return jsonify({"message": "Ubicación agregada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/nearby", methods=["GET"])
def nearby():
    group = request.args.get("group")
    lon = float(request.args.get("lon"))
    lat = float(request.args.get("lat"))
    result = get_nearby(group, lon, lat)
    return jsonify(result)

@app.route("/distance", methods=["GET"])
def distance():
    group   = request.args.get("group")
    place_name    = request.args.get("name")
    user_id = request.args.get("user_id")
    print(place_name)
    dist    = get_distance_between_user_and_place(user_id,place_name,group)
    
    return jsonify({"km": dist})

@app.route("/places", methods=["GET"])
def places():
    group = request.args.get("group")
    if not group:
        return jsonify({"error": "Falta el grupo"}), 400
    result = get_all_places(group)
    return jsonify(result)

@app.route("/update_location", methods=["POST"])
def update_location():
    print(request.get_json())
    data = request.get_json()
    user_id = data.get('user_id')  # un identificador de usuario
    lat = data.get('lat')
    lon = data.get('lon')

    if not all([user_id, lat, lon]):
        return jsonify({"error": "Faltan datos"}), 400

    save_user_location(user_id, lon, lat)
    return jsonify({"message": "Ubicación actualizada"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)