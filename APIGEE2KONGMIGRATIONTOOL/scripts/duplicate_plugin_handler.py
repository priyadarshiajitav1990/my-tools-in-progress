#!/usr/bin/env python3
"""
Handle duplicate Kong plugin configuration in API migration, following robust best practices and fallback options.
"""
import os
import json

def find_duplicate_plugins(plugin_list):
    seen = {}
    duplicates = []
    for plugin in plugin_list:
        name = plugin.get('name')
        if name:
            if name in seen:
                duplicates.append((name, seen[name], plugin))
            else:
                seen[name] = plugin
    return duplicates

def check_alternative_plugin(plugin_name, alternatives_map):
    return alternatives_map.get(plugin_name)

def merge_plugin_configs(config1, config2):
    merged = config1.copy()
    for k, v in config2.items():
        if k not in merged:
            merged[k] = v
        elif isinstance(merged[k], list) and isinstance(v, list):
            merged[k] = list(set(merged[k] + v))
        elif isinstance(merged[k], dict) and isinstance(v, dict):
            merged[k].update(v)
        # else: keep first config's value
    return merged

def suggest_lua_script(plugin_name):
    return f"Use pluginsfunctionailtieslua/{plugin_name}_handler.lua with luaexecuter plugin for dynamic configuration."

def handle_duplicate_plugins(plugin_list, alternatives_map):
    duplicates = find_duplicate_plugins(plugin_list)
    handled = []
    for name, first, second in duplicates:
        print(f"Duplicate plugin detected: {name}")
        # 1. Check for alternative plugin
        alt = check_alternative_plugin(name, alternatives_map)
        if alt:
            print(f"  Alternative plugin available: {alt}. Use instead of duplicate.")
            handled.append({'plugin': name, 'action': 'use_alternative', 'alternative': alt})
            continue
        # 2. Try merging configs
        merged_config = merge_plugin_configs(first.get('config', {}), second.get('config', {}))
        if merged_config != first.get('config', {}):
            print(f"  Merged configs for {name}. Use single plugin with merged config.")
            handled.append({'plugin': name, 'action': 'merge_configs', 'config': merged_config})
            continue
        # 3. Suggest Lua script
        lua_suggestion = suggest_lua_script(name)
        print(f"  No alternative or merge possible. {lua_suggestion}")
        handled.append({'plugin': name, 'action': 'use_lua_script', 'lua_script': lua_suggestion})
        # 4. Fallback: custom plugin (details to be provided by user)
        print(f"  If Lua script is insufficient, create a custom Kong plugin for {name}.")
        handled.append({'plugin': name, 'action': 'custom_plugin'})
    return handled

def main():
    # Example usage: load plugins from a JSON file (replace with actual input)
    plugins_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mappers/plugins_example.json')
    alternatives_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mappers/plugin_alternatives.json')
    if os.path.exists(plugins_path):
        with open(plugins_path) as f:
            plugin_list = json.load(f)
    else:
        plugin_list = []
    if os.path.exists(alternatives_path):
        with open(alternatives_path) as f:
            alternatives_map = json.load(f)
    else:
        alternatives_map = {}
    handle_duplicate_plugins(plugin_list, alternatives_map)

if __name__ == "__main__":
    main()
