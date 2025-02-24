import json
import os

CONFIG_FILE = "favzen-config.json"


def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
    # Default configuration values
    if "sort_order" not in config:
        config["sort_order"] = "Alphabetical (A-Z)"
    if "theme" not in config:
        config["theme"] = "dark"
    if "visible_columns" not in config:
        config["visible_columns"] = [True, True, True, True]
    return config


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
