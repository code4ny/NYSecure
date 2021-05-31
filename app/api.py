from flask import jsonify

from app import app
from app.config import BASE_API_PATH, DATABASE_URI
from app.database import DataStore
from app.vars import BLOCKS

ds = DataStore()


@app.route(BASE_API_PATH + "/locationdata")
def get_location_data():
    """Query location datas for api.

    Returns:
        json: has the following schema:
              {
                <block_name> (str):
                  {
                    <level> (single digit str): <people there> (int)
                  }
              }
    """
    datas = {}
    for block in BLOCKS:
        datas[block] = {}
        for level in range(1, 6):
            result = ds.get_summary(block=block, level=str(level))
            if result is not None:
                result = sum(result.values())
            datas[block][level] = result

    return jsonify(datas)
