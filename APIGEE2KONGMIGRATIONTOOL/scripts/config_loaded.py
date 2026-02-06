#!/usr/bin/env python3
"""
Load config.json and set all values as environment variables and global variables for use by other scripts.
"""

import os
import json
import sys
import glob

CONFIG_GLOBAL = {}
MAPPERS_GLOBAL = {}


def flatten_dict(d, parent_key='', sep='__'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def load_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return config

def set_env_vars_from_config(config):
    flat = flatten_dict(config)
    for k, v in flat.items():
        if v is None:
            continue
        os.environ[k.upper()] = str(v)
    return flat

def load_all_mappers(mappers_dir):
    mappers = {}
    for json_file in glob.glob(os.path.join(mappers_dir, '*.json')):
        name = os.path.splitext(os.path.basename(json_file))[0]
        with open(json_file) as f:
            try:
                mappers[name] = json.load(f)
            except Exception as e:
                mappers[name] = {'error': str(e)}
    return mappers

def config_loaded():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../configs/config.json')
    config = load_config(config_path)
    global CONFIG_GLOBAL
    CONFIG_GLOBAL = config
    set_env_vars_from_config(config)
    # Load all mappers
    mappers_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mappers')
    global MAPPERS_GLOBAL
    MAPPERS_GLOBAL = load_all_mappers(mappers_dir)
    print("Config and all mappers loaded. Environment variables set.")

if __name__ == "__main__":
    config_loaded()
if __name__ == "__main__":
    config_loaded()
