import os


class ConfigFiles:
    from .event_controller import EventController
    from .config_element import ConfigElement

    def __init__(self, *,
                 config_name: str,
                 work_directory,
                 name: str,
                 config_elements: dict[str, ConfigElement],
                 new_config_elements: dict[str, ConfigElement],
                 event_controller: EventController):
        self.__config_name: str = config_name
        self.__work_directory: str = work_directory
        self.__name: str = name

        from .config_element import ConfigElement
        self.__config_elements: dict[str, ConfigElement] = config_elements
        self.__new_config_elements: dict[str, ConfigElement] = new_config_elements

        from .event_controller import EventController
        self.__event_controller: EventController = event_controller

    def file_is_exist(self) -> bool:
        return os.path.exists(os.path.join(self.__work_directory, self.__name))

    def create_config_file(self) -> None:
        if self.file_is_exist() is False:
            with open(os.path.join(self.__work_directory, self.__name), mode='w', encoding='utf-8') as file:
                for key, value in self.__config_elements.items():
                    file.write(f'# {value.description} - [{value.data_type}] \n'
                               f'{value.name} = {value.value}\n\n')

            self.__event_controller.create_event(event_type=2, message=f'Config file [{self.__name}] created]')

    def read_config_file(self):
        from .config_element import ConfigElement
        from .data_types import ConfigDataTypes

        if self.file_is_exist() is False:
            raise FileNotFoundError(f'Config file [{self.__name}] not found.')

        try:
            temp: dict[str, ConfigElement] = {}
            with open(os.path.join(self.__work_directory, self.__name), mode='r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()

                    if len(line) == 0:
                        continue

                    if line.startswith('#'):
                        continue

                    if '=' not in line:
                        raise TypeError(f'Config file [{self.__name}] contains invalid syntax.')

                    element_name, element_value = line.split('=')

                    config_data_types: ConfigDataTypes = ConfigDataTypes()

                    for name, value in self.__config_elements.items():
                        if name == element_name.strip():

                            self.__check_dependency(
                                dependency_element_name=value.dependency,
                                current_element_name=name,
                                current_element_value=element_value,
                                new_config_elements=temp
                            )

                            temp[name] = ConfigElement(
                                config_name=self.__config_name,
                                name=name,
                                data_type=config_data_types.get_enum_by_value(value.data_type),
                                value=element_value.strip(),
                                required=value.required,
                                description=value.description,
                                dependency=value.dependency)
                self.__event_controller.create_event(event_type=3, message=f'Config file [{self.__name}] read]')
                return temp
        except Exception as e:
            raise Exception(f'Failed to read config file [{self.__name}] due to: {e}')

    @staticmethod
    def __check_dependency(*,
                           dependency_element_name: str,
                           current_element_name: str,
                           current_element_value: str,
                           new_config_elements: dict[str, ConfigElement]) -> bool:
        from .data_types import ConfigDataTypesEnum


        if dependency_element_name is None or dependency_element_name.strip() == '':
            return True

        for element_name, element_value in new_config_elements.items():
            if element_name == dependency_element_name.strip():
                if element_value.data_type == ConfigDataTypesEnum.BOOLEAN.value:
                    if element_value.value is True:
                        if len(current_element_value.strip()) == 0 or current_element_value.strip().lower() == 'none':
                            raise ValueError(f"Element [{current_element_name}] can't be empty")
                        else:
                            return True
                    else:
                        return True
                else:
                    raise TypeError(f"The element on which the dependency is [{dependency_element_name.strip()}] must be of type [bool]")
        raise Exception(f'Dependency [{dependency_element_name.strip()}] not found.')
