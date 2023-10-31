import json

CONFIG_FILE = "config.json"


def get_config(config_file):
    config_obj = {}
    with open(config_file, encoding="utf-8") as f:
        config_obj = json.load(f)
    return config_obj
