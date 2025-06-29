from typing import Optional, Any


class ConfigElement:
    from data_types import ConfigDataTypesEnum
    def __init__(self, *,
                 config_name: str,
                 name: str,
                 data_type: ConfigDataTypesEnum,
                 value: Optional[Any] = None,
                 required: bool = True,
                 description: Optional[Any] = None,
                 dependency: Optional[str] = None):
        self.__config_name: str = config_name
        self.__name: str = name
        self.__data_type: str = data_type.value
        self.__required: bool = required
        self.__value: Optional[Any] = self.__convert_to_data_type(value)
        self.__description: Optional[str] = description
        self.__dependency: str = dependency

        from data_types import ConfigDataTypes
        self.__data_types: ConfigDataTypes = ConfigDataTypes()
        self.__check_data_type(self.__data_type)

    def __check_data_type(self, data_type: str):
        if data_type not in self.__data_types.get_data_types():
            raise TypeError(f'Data type "{data_type}" is not supported for element {self.__name}.')
        else:
            self.__data_type = data_type

    def __convert_to_data_type(self, value: Optional[Any] = None):
        from data_types import ConfigDataTypesEnum

        if (value is None or len(value) == 0  or value == 'None') and self.__required is False:
            return None

        if (value is None or len(value) == 0 or value == 'None') and self.__required is True:
            raise TypeError(f'Value for element [{self.__name}] is required.')

        try:
            if self.__data_type == ConfigDataTypesEnum.STRING.value:
                return str(value)
            elif self.__data_type == ConfigDataTypesEnum.INTEGER.value:
                return int(value)
            elif self.__data_type == ConfigDataTypesEnum.FLOAT.value:
                if '.' not in value:
                    raise TypeError(f'Wrong value for [{self.__data_type}] element [{self.__name}]')
                return float(value)
            elif self.__data_type == ConfigDataTypesEnum.BOOLEAN.value:
                if isinstance(value, str):
                    if value.lower() == 'true':
                        return True
                    elif value.lower() == 'false':
                        return False
                elif isinstance(value, bool):
                    return value
                raise TypeError(f'Wrong value for [{self.__data_type}] element [{self.__name}].')
            elif self.__data_type == ConfigDataTypesEnum.LIST.value:
                if isinstance(value, str):
                    value = value.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
                    result = [item.strip() for item in value.split(',') if item.strip()]
                    return result
                elif isinstance(value, list):
                    return value
                else:
                    raise TypeError(f'Cannot convert value to list for element [{self.__name}].')
            else:
                raise TypeError(f'Data type [{self.__data_type}] is not supported for element [{self.__name}].')
        except Exception as e:
            raise ValueError(f'Failed to convert [{value}] to type [{self.__data_type}] in configuration element [{self.__config_name.strip()}] - [{e}]')

    @property
    def name(self) -> str:
        return self.__name

    @property
    def data_type(self) -> str:
        return self.__data_type

    @property
    def value(self) -> Any:
        return self.__value

    @property
    def required(self) -> bool:
        return self.__required

    @property
    def dependency(self) -> str:
        return self.__dependency

    @property
    def description(self) -> str:
        return self.__description

    @name.setter
    def name(self, name: str):
        self.__name = name

    @data_type.setter
    def data_type(self, data_type: ConfigDataTypesEnum):
        self.__data_type = data_type

    @value.setter
    def value(self, value: Any):
        self.__value = value

    @required.setter
    def required(self, required: bool):
        self.__required = required

    @description.setter
    def description(self, description: str):
        self.__description = description

    @dependency.setter
    def dependency(self, dependency: str):
        self.__dependency = dependency
