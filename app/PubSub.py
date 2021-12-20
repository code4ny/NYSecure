from typing import Union


class Publisher:
    """Allows for subscriber to be notified of event without the publisher caring who is listening.

    Implementation of **observer design pattern**. 
    """

    def __init__(self) -> None:
        self.subscribers: set["Subscriber"] = set()

    def __repr__(self) -> str:
        return f"Publisher({self.subscribers})"

    def add_subscriber(self, subscriber: "Subscriber") -> None:
        """Add a subscriber to the publisher.

        Args:
            subscriber (Subscriber): the subscriber to be added
        """
        self.subscribers.add(subscriber)
        return

    def remove_subscriber(self, sub_name: str) -> Union["Subscriber", None]:
        """Remove a subscriber from publisher by its name.

        Args:
            sub_name (str): the name of the subscriber

        Returns:
            Subscriber: if it is successfully deleted, else return none
        """

        for i, sub in enumerate(self.subscribers):
            if sub.name == sub_name:
                return self.subscribers.pop(i)
        return

    def notify(self, event: str):
        """Notify all the subscriber about an event

        Args:
            event (str): the name of the event
        """
        for sub in self.subscribers:
            sub.notify(event)


class Subscriber:
    """Listen for event by the subscriber
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Subscriber({self.name})"

    def notify(self, event: str):
        """The method called by the Publisher to publish an event

        Args:
            event (str): the name of the event

        Raises:
            NotImplementedError: Must be implemented by a child class.
        """
        raise NotImplementedError
