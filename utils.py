# utils.py

import os
import json

CONFIG_PATH = "assets/config/config.json"
VERSION_PATH = "assets/config/version.json"
DEFAULT_VERSION = "1.0.0"

default_config = {
    "ashita_exe": "",
    "windower_exe": "",
    "xi_loader_exe": "assets/config/xiLoader.exe"
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as file:
            return json.load(file)
    return default_config

def save_config(config):
    with open(CONFIG_PATH, 'w') as file:
        json.dump(config, file, indent=4)

def load_version():
    if os.path.exists(VERSION_PATH):
        with open(VERSION_PATH, 'r') as file:
            version_data = json.load(file)
            return version_data.get("launcher_version", DEFAULT_VERSION)
    return DEFAULT_VERSION

