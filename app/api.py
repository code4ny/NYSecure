from app.config import BASE_API_PATH, DATABASE_URI
from app import app
from flask import jsonify
from app.database import DataStore

ds = DataStore()
BLOCKS = ['science', 'main']


@app.route(BASE_API_PATH + "/locationdata")
def get_location_data():
    datas = {}
    for block in BLOCKS:
        datas[block] = {}
        for level in range(1, 6):
            datas[block][level] = ds.get_summary(block=block, level="l" + str(level))

    return jsonify(datas)
