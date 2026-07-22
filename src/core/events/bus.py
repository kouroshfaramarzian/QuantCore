class EventBus:

    def __init__(self):

        self._subscribers = {}

    def subscribe(

        self,

        event_name,

        callback,

    ):

        self._subscribers.setdefault(

            event_name,

            [],

        ).append(callback)

    def publish(

        self,

        event,

    ):

        for callback in self._subscribers.get(

            event.name,

            [],

        ):

            callback(event)