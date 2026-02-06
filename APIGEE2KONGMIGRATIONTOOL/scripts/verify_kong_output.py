#!/usr/bin/env python3
"""
Verify possible ordering of Kong API plugins in the output YAML/JSON, and ensure each service, route, and plugin has a tag with the Apigee API name.
"""
import os
import yaml
import json

def load_output_file(output_path):
    with open(output_path) as f:
        if output_path.endswith('.yaml') or output_path.endswith('.yml'):
            return yaml.safe_load(f)
        else:
            return json.load(f)

def verify_plugin_ordering(kong_config):
    ordering_ok = True
    missing_ordering = []
    for service in kong_config.get('services', []):
        plugins = service.get('plugins', [])
        plugin_names = [p['name'] for p in plugins]
        if len(plugin_names) != len(set(plugin_names)):
            print(f"Duplicate plugin detected in service {service.get('name')}")
            ordering_ok = False
        for p in plugins:
            if not p.get('after') and not p.get('before'):
                missing_ordering.append(f"plugin:{p.get('name')} in service:{service.get('name')}")
    for route in kong_config.get('routes', []):
        plugins = route.get('plugins', [])
        plugin_names = [p['name'] for p in plugins]
        if len(plugin_names) != len(set(plugin_names)):
            print(f"Duplicate plugin detected in route {route.get('name')}")
            ordering_ok = False
        for p in plugins:
            if not p.get('after') and not p.get('before'):
                missing_ordering.append(f"plugin:{p.get('name')} in route:{route.get('name')}")
    return ordering_ok, missing_ordering

def verify_apigee_tag(kong_config):
    missing_tags = []
    for service in kong_config.get('services', []):
        if 'apigee_api_name' not in service:
            missing_tags.append(f"service:{service.get('name')}")
        for plugin in service.get('plugins', []):
            if 'apigee_api_name' not in plugin:
                missing_tags.append(f"plugin:{plugin.get('name')} in service:{service.get('name')}")
    for route in kong_config.get('routes', []):
        if 'apigee_api_name' not in route:
            missing_tags.append(f"route:{route.get('name')}")
        for plugin in route.get('plugins', []):
            if 'apigee_api_name' not in plugin:
                missing_tags.append(f"plugin:{plugin.get('name')} in route:{route.get('name')}")
    return missing_tags

def verify_kong_output(output_path):
    kong_config = load_output_file(output_path)
    print(f"Verifying plugin ordering and Apigee tags in {output_path}...")
    ordering_ok, missing_ordering = verify_plugin_ordering(kong_config)
    missing_tags = verify_apigee_tag(kong_config)
    if ordering_ok:
        print("No duplicate plugins detected in any service or route.")
    else:
        print("Duplicate plugins found. See above.")
    if not missing_tags:
        print("All services, routes, and plugins have apigee_api_name tags.")
    else:
        print("Missing apigee_api_name tags:")
        for tag in missing_tags:
            print(f"  {tag}")
    if not missing_ordering:
        print("All plugins have 'after' or 'before' ordering configured.")
    else:
        print("Missing 'after'/'before' ordering for:")
        for tag in missing_ordering:
            print(f"  {tag}")
    return ordering_ok and not missing_tags and not missing_ordering

def main():
    # Example usage: pass output file path as argument
    import sys
    if len(sys.argv) != 2:
        print("Usage: python verify_kong_output.py <output.yaml|output.json>")
        sys.exit(1)
    output_path = sys.argv[1]
    verify_kong_output(output_path)

if __name__ == "__main__":
    main()
