from typing import Type

from flask_sse import sse

from app.database import DataStore
from PubSub import Subscriber


class LocationDataStream(Subscriber):
    "A singleton class to help with the streaming of data for sse"
    __instance__ = None

    def __new__(cls: Type["LocationDataStream"], *args, **kwargs) -> "LocationDataStream":
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        self.name = 'LocationDataStream'
        self.ds = DataStore()

    def notify(self, event: str):
        if event == "loc-updates":
            return self.stream_location_data()

    def stream_location_data(self):
        sse.publish(self.ds.return_location_data(),
                    type='locationdata-updates')
        return "published"
