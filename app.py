from bson import ObjectId
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

connection_url = "mongodb+srv://test:sparta@learningx.obnyi.mongodb.net/?retryWrites=true&w=majority&appName=LearningX"
db_name = "certification"

client = MongoClient(connection_url)
db = client[db_name]


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/vehicle")
def input_data():
    return render_template("vehicles_input.html")


@app.route("/vehicle/update/<id>")
def update_data(id):
    vehicle = db.vehicles.find_one({"_id": ObjectId(id)})

    return render_template("vehicles_update.html", vehicle=vehicle)


@app.route("/api/get", methods=["GET"])
def get():
    vehicles_list = list(db.vehicles.find({}))

    for vehicle in vehicles_list:
        vehicle["_id"] = str(vehicle["_id"])

    return jsonify({"vehicles": vehicles_list})


@app.route("/api/save", methods=["POST"])
def save():
    owner = request.form["owner_give"]
    vehicle = request.form["vehicle_give"]
    merk = request.form["merk_give"]
    license = request.form["license_give"]

    doc = {
        "owner": owner,
        "vehicle": vehicle,
        "merk": merk,
        "license": license,
    }

    db.vehicles.insert_one(doc)

    return jsonify({"result": "success", "msg": "data successfully saved!"})


@app.route("/api/delete", methods=["POST"])
def delete():
    id = request.form["id_give"]
    db.vehicles.delete_one({"_id": ObjectId(id)})

    return jsonify({"result": "success", "msg": "data successfully deleted!"})


@app.route("/api/update", methods=["POST"])
def update():
    id = request.form["id_give"]

    owner = request.form["owner_give"]
    vehicle = request.form["vehicle_give"]
    merk = request.form["merk_give"]
    license = request.form["license_give"]

    db.vehicles.update_one(
        {
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "owner": owner,
                    "vehicle": vehicle,
                    "merk": merk,
                    "license": license,
                }
            },
        }
    )

    return jsonify({"result": "success", "msg": "data successfully updated!"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
