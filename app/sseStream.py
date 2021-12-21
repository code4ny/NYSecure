import queue
import time
from typing import Type

from app.database import DataStore
from app.PubSub import Subscriber


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


class LocationDataStream(Subscriber):
    "A singleton class to help with the streaming of data for sse"
    __instance__ = None

    def __new__(cls: Type["LocationDataStream"], *args, **kwargs) -> "LocationDataStream":
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        self.name = 'LocationDataStream'
        ds = DataStore()
        ds.add_subscriber(self)
        self.last_time = time.time()
        self.data = queue.Queue(maxsize=5)

    def __hash__(self):
        return hash(self.name)

    def notify(self, event: str):
        if event == "loc-updates":
            print('notified', event)
            try:
                self.data.put(
                    format_sse(
                        'new update',
                        event="location-updates"))
                print(self.data.queue)
            except queue.Full:
                print('emptying')
                while not self.data.empty:
                    self.data.get_nowait()
                # retry to add the new update
                self.notify('loc-updates')

    def stream_location_data(self):
        while 1:
            time.sleep(2)
            # heroku have max 55 seconds
            is_timeout: bool = time.time() - self.last_time > 40

            if not self.data.empty:
                yield self.data.get()
            elif is_timeout:
                print('ping')
                self.last_time = time.time()
                yield 'data: ping\n\n'
