import os
import yaml

config_yaml = '/config/config.yml'
yaml_path = os.path.dirname(__file__) + config_yaml

with open(yaml_path, 'r') as yml:
    config = yaml.safe_load(yml)
    filepath = config['FilePath']
    socket_info = config['Socket']


if __name__ == '__main__':
    print(config)
