
class ConfigEvent:
    def __init__(self, *, event_type: int, message: str):
        self.__event_type: int = event_type
        self.__message: str = message

    @property
    def event_type(self) -> int:
        return self.__event_type

    @property
    def message(self) -> str:
        return self.__message

