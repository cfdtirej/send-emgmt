import yaml

config_yaml = 'config/config.yml'
with open(config_yaml, 'r') as yml:
    config = yaml.safe_load(yml)
    latest_path = config['Path']['LatestLog']
    prev_path = config['Path']['PrevLog']
    host = config['Socket']['HOST']
    port = config['Socket']['PORT']

if __name__ == '__main__':
    print(latest_path)
    print(prev_path)