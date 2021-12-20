from flask import Response, jsonify

from app import app
from app.config import BASE_API_PATH
from app.database import DataStore
from app.sseStream import LocationDataStream

ds = DataStore()
stream = LocationDataStream()


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

@app.route(BASE_API_PATH + "/stream/locationdata_update")
def location_data_stream():
    """Emit new EventSource
    """
    return Response(stream.stream_location_data(), mimetype="text/event-stream")
