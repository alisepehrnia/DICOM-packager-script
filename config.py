import yaml

default_config_file_path = "config.yaml"

def read_config(file: str = default_config_file_path):
    try:
        with open(file, mode="r") as f:
            cfg = yaml.safe_load(f)
            return cfg
    except:
        return {}

def parse_config(data: str):
    try:
        return yaml.load(data)
    except:
        return {}