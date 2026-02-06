#!/usr/bin/env python3
"""
Recursively walk an unzipped Apigee API bundle, parse all XML files, and create a JSON file with each XML file as a separate entity containing all its information (no data loss).
The JSON file will mirror the bundle structure and be placed under the respective unzipped API bundle folder.
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from collections import OrderedDict

def get_bundle_dir():
    if len(sys.argv) != 2:
        print("Usage: python apigee_bundle_xml2json.py <unzipped_api_bundle_dir>")
        sys.exit(1)
    return sys.argv[1]

def xml_to_dict(elem):
    d = OrderedDict()
    d['tag'] = elem.tag
    d['attrib'] = dict(elem.attrib)
    d['text'] = elem.text.strip() if elem.text and elem.text.strip() else ''
    d['children'] = [xml_to_dict(child) for child in elem]
    return d

def collect_xml_files(root_dir):
    xml_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith('.xml'):
                xml_files.append(os.path.join(dirpath, f))
    return xml_files

def parse_and_build_json(bundle_dir, xml_files):
    bundle_json = OrderedDict()
    for xml_path in xml_files:
        rel_path = os.path.relpath(xml_path, bundle_dir)
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            bundle_json[rel_path] = xml_to_dict(root)
        except Exception as e:
            bundle_json[rel_path] = {'error': str(e)}
    return bundle_json

def write_json(bundle_dir, bundle_json):
    json_path = os.path.join(bundle_dir, 'apigee_bundle.json')
    with open(json_path, 'w') as f:
        json.dump(bundle_json, f, indent=2)
    print(f"Wrote {json_path} with {len(bundle_json)} XML entities.")

def apigee_bundle_xml2json():
    bundle_dir = get_bundle_dir()
    xml_files = collect_xml_files(bundle_dir)
    bundle_json = parse_and_build_json(bundle_dir, xml_files)
    write_json(bundle_dir, bundle_json)

if __name__ == "__main__":
    apigee_bundle_xml2json()
