#!/usr/bin/env python3
"""
Extract Apigee API proxy structure, endpoints, flows, policies, and traffic forwarding logic from unzipped bundle and store in a structured JSON file under the bundle folder.
"""

import os
import xml.etree.ElementTree as ET
import json

def get_api_name(bundle_dir):
    apiproxy_xml = os.path.join(bundle_dir, 'apiproxy', 'apiproxy.xml')
    if os.path.exists(apiproxy_xml):
        tree = ET.parse(apiproxy_xml)
        root = tree.getroot()
        name = root.findtext('Name')
        return name
    return os.path.basename(bundle_dir)

def get_endpoints(bundle_dir, endpoint_type):
    endpoints_dir = os.path.join(bundle_dir, 'apiproxy', endpoint_type)
    endpoints = []
    if os.path.isdir(endpoints_dir):
        for f in os.listdir(endpoints_dir):
            if f.endswith('.xml'):
                endpoints.append(os.path.splitext(f)[0])
    return endpoints

def parse_flows(endpoint_xml_path):
    flows = []
    if os.path.exists(endpoint_xml_path):
        tree = ET.parse(endpoint_xml_path)
        root = tree.getroot()
        for flow in root.findall('.//Flow'):
            flow_info = {
                'name': flow.get('name'),
                'condition': flow.findtext('Condition'),
                'policies': []
            }
            for step in flow.findall('.//Step'):
                policy = step.findtext('Name')
                cond = step.findtext('Condition')
                flow_info['policies'].append({'policy': policy, 'condition': cond})
            flows.append(flow_info)
    return flows

def get_proxy_structure(bundle_dir):
    structure = {
        "api_name": get_api_name(bundle_dir),
        "endpoints": {
            "proxy": get_endpoints(bundle_dir, "proxies"),
            "target": get_endpoints(bundle_dir, "targets")
        },
        "resources": get_resources_tree(os.path.join(bundle_dir, "apiproxy", "resources"), bundle_dir)
    }
    return structure

def get_resources_tree(resources_dir, bundle_dir):
    resources_tree = {}
    for root, dirs, files in os.walk(resources_dir):
        rel_root = os.path.relpath(root, resources_dir)
        if rel_root == '.':
            rel_root = ''
        folder = resources_tree
        if rel_root:
            for part in rel_root.split(os.sep):
                folder = folder.setdefault(part, {})
        folder['files'] = files
    return resources_tree

def print_tree(startpath, prefix=''):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_apigee_api_structure.py <unzipped_api_bundle_dir>")
        sys.exit(1)
    bundle_dir = sys.argv[1]
    api_name = get_api_name(bundle_dir)
    print("\n___ API Filesystem Tree ___")
    print_tree(bundle_dir)
    structure = get_proxy_structure(bundle_dir)
    print("\n___ API Structure ___")
    print(json.dumps(structure, indent=2))
    # Save to interim json file
    interim_dir = os.path.join(os.path.dirname(bundle_dir), '..', 'interims')
    os.makedirs(interim_dir, exist_ok=True)
    interim_path = os.path.join(interim_dir, f"{api_name}_filesystem.json")
    with open(interim_path, 'w') as f:
        json.dump(structure, f, indent=2)
    print(f"\nAPI structure written to {interim_path}")

if __name__ == "__main__":
    main()
