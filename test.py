import os

from config import Config, ConfigEvent, ConfigDataTypesEnum

def event_print(event: ConfigEvent):
    print(f'{event.event_type}: {event.message}')


config: Config = Config(os.path.dirname(__file__), 'test')
config.add_event_listener(event_print)


config.create_element(name='element', data_type=ConfigDataTypesEnum.STRING, value='', required=False, description='element')
config.create_element(name='element1', data_type=ConfigDataTypesEnum.STRING, value='test', required=True, description='element1')
config.create_element(name='element2', data_type=ConfigDataTypesEnum.INTEGER, value='1', required=True)
config.create_element(name='element3', data_type=ConfigDataTypesEnum.FLOAT, value='0.001', required=True)
config.create_element(name='element4', data_type=ConfigDataTypesEnum.BOOLEAN, value='True', required=False)
config.create_element(name='element5', data_type=ConfigDataTypesEnum.LIST, value='1', required=False, dependency='element4')
config.create_config_file()
config.read_config_file()

print(config.get(name='element'))
print(config.get(name='element1'))
print(config.get(name='element2'))
print(config.get(name='element3'))
print(config.get(name='element4'))
print(config.get(name='element5'))