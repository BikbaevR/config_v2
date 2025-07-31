
from typing import Any, Optional, Callable
from .config_element import ConfigElement
from .config_event import ConfigEvent
from .data_types import ConfigDataTypesEnum
from .event_controller import EventController


class Config:
    def __init__(self, work_directory: str, name: str):
        self.__work_directory: str = work_directory
        self.__name: str = name + '.cfg'

        self.__config_elements: dict[str, ConfigElement] = {}
        self.__new_config_elements: dict[str, ConfigElement] = {}

        self.__event_controller: EventController = EventController()

        from .config_files import ConfigFiles
        self.__config_file: ConfigFiles = ConfigFiles(
            config_name=self.__name,
            work_directory=self.__work_directory,
            name=self.__name,
            config_elements=self.__config_elements,
            new_config_elements=self.__new_config_elements,
            event_controller=self.__event_controller
        )

    def create_element(self, *,
                        name: str,
                        data_type: ConfigDataTypesEnum,
                        value: Optional[Any] = None,
                        required: bool = True,
                        description: Optional[Any] = None,
                        dependency: Optional[str] = None):
        try:
            self.__check_duplicate_name(name)
            self.__config_elements[name] = ConfigElement(
                config_name=self.__name,
                name=name,
                data_type=data_type,
                value=value,
                required=required,
                description=description,
                dependency=dependency,
                config_file=self.__config_file
            )

            self.__event_controller.create_event(event_type=1, message=f'Element "{name}" created')
        except Exception as e:
            raise Exception(f'Error while creating element [{name}]: {e}')

    def get(self, name: str) -> Any:
        try:
            return self.__new_config_elements[name].value
        except Exception:
            raise Exception(f'Element [{name}] not found')

    def create_config_file(self):
        self.__config_file.create_config_file()

    def read_config_file(self):
        self.__new_config_elements = self.__config_file.read_config_file()

    def add_event_listener(self, listener: Callable[[ConfigEvent], None]):
        self.__event_controller.add_listeners(listener)

    def __check_duplicate_name(self, name: str):
        if name in self.__config_elements:
            raise ValueError(f'Duplicate name for element [{name}]')
