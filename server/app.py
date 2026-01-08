#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

# ---------------------------
# Routes / Views
# ---------------------------


@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    """
    Return a single earthquake by ID.
    """
    quake = Earthquake.query.filter_by(id=id).first()

    if quake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

    return jsonify({
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    }), 200


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    """
    Return all earthquakes with magnitude >= the provided value.
    """
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quake_dicts = [
        {
            "id": q.id,
            "location": q.location,
            "magnitude": q.magnitude,
            "year": q.year
        }
        for q in quakes
    ]

    return jsonify({
        "count": len(quake_dicts),
        "quakes": quake_dicts
    }), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
