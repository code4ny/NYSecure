from app.config import BASE_API_PATH, DATABASE_URI
from app import app
from flask import jsonify


@app.route(BASE_API_PATH + "/locationdata")
def get_location_data():
    return jsonify()
