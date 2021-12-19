from flask import jsonify

from app import app
from app.config import BASE_API_PATH
from app.database import DataStore

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
                  },...
              }
    """
    return jsonify(ds.return_location_data())
