from flask import jsonify, Response

from app import app
from app.config import BASE_API_PATH
from app.database import DataStore
from app.sseStream import LocationDataStream

ds = DataStore()
stream = LocationDataStream()
ds.add_subscriber(stream)

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

@app.route(BASE_API_PATH + "/stream/locationdata")
def location_data_stream():
    """Query location datas for api.

    Returns:
        text of json: has the following schema:
              {
                <block_name> (str):
                  {
                    <level> (single digit str): <people there> (int)
                  },...
              }
    """
    return Response(stream.stream_location_data(), mimetype="text/event-stream")
