#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the migration engine and the database
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Earthquake Tracker API</h1>'

# Task #3: Get an earthquake by id
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query the database for a specific ID
    quake = Earthquake.query.filter_by(id=id).first()
    
    if quake:
        # If found, return the dictionary representation (from SerializerMixin)
        return make_response(quake.to_dict(), 200)
    else:
        # If not found, return a 404 with the specific error message
        return make_response({"message": f"Earthquake {id} not found."}, 404)

# Task #4: Get earthquakes matching a minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_quakes_by_magnitude(magnitude):
    # Use .filter() for the relational operator >=
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Structure the response as required by the lab
    response_dict = {
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }
    
    return make_response(response_dict, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
