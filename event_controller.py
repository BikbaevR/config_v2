from .config_event import ConfigEvent


class EventController:
    from typing import Callable

    def __init__(self):
        from typing import List, Callable
        self.__listeners: List[Callable[[ConfigEvent], None]] = []

    def add_listeners(self, listener: Callable[[ConfigEvent], None]):
        self.__listeners.append(listener)

    def create_event(self,event_type: int, message: str):
        event = ConfigEvent(event_type=event_type, message=message)

        for listener in self.__listeners:
            listener(event)
