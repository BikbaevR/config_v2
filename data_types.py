from enum import Enum

class ConfigDataTypesEnum(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"


class ConfigDataTypes:
    __instance: 'ConfigDataTypes' = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.__dataType: list = [dataType.value for dataType in ConfigDataTypesEnum]
            self.__initialized = True

    def get_data_types(self) -> list:
        return self.__dataType

    def get_enum_by_value(self, value: str) -> ConfigDataTypesEnum:
        for item in ConfigDataTypesEnum:
            if item.value == value:
                return item
        raise ValueError(f'Unknown enum value: {value}')

__data_types: ConfigDataTypes = ConfigDataTypes()
