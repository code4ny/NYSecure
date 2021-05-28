from app.config import BASE_API_PATH, DATABASE_URI
from app import app
from flask import jsonify
from app.database import DataStore
from app.location_variables import BLOCKS

ds = DataStore()


@app.route(BASE_API_PATH + "/locationdata")
def get_location_data():
    datas = {}
    for block in BLOCKS:
        datas[block] = {}
        for level in range(1, 6):
            datas[block][level] = ds.get_summary(block=block, level="l" + str(level))

    return jsonify(datas)
