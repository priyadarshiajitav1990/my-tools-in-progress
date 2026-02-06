#!/usr/bin/env python3
"""
Detect Apigee API proxy type (OPDK, X, Hybrid) from an unzipped API bundle and print the file system tree.
"""

import os
import sys

def get_bundle_path():
    if len(sys.argv) != 2:
        print("Usage: python detect_apigee_type_and_tree.py <unzipped_api_bundle_dir>")
        sys.exit(1)
    return sys.argv[1]

def detect_apigee_type(bundle_path):
    apiproxy_dir = os.path.join(bundle_path, 'apiproxy')
    if not os.path.isdir(apiproxy_dir):
        return 'Unknown'
    files = os.listdir(apiproxy_dir)
    if 'apiproxy.xml' in os.listdir(bundle_path):
        return 'OPDK'
    if 'apiproxy.yaml' in os.listdir(bundle_path):
        return 'X/Hybrid'
    for f in files:
        if f.endswith('.yaml'):
            return 'X/Hybrid'
    if 'edge.json' in os.listdir(bundle_path):
        return 'X/Hybrid'
    return 'OPDK'

def print_tree(startpath, prefix=''):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')
        if level == 0:
            for d in dirs:
                print_tree(os.path.join(root, d), prefix + '  ')
            break

def detect_apigee_type_and_tree():
    bundle_path = get_bundle_path()
    apigee_type = detect_apigee_type(bundle_path)
    print(f"Detected Apigee API Proxy Type: {apigee_type}")
    print("File System Tree:")
    print_tree(bundle_path)

if __name__ == "__main__":

    def detect_apigee_type(bundle_path):
        apiproxy_dir = os.path.join(bundle_path, 'apiproxy')
        if not os.path.isdir(apiproxy_dir):
            return 'Unknown'
        files = os.listdir(apiproxy_dir)
        if 'apiproxy.xml' in os.listdir(bundle_path):
            return 'OPDK'
        if 'apiproxy.yaml' in os.listdir(bundle_path):
            return 'X/Hybrid'
        for f in files:
            if f.endswith('.yaml'):
                return 'X/Hybrid'
        if 'edge.json' in os.listdir(bundle_path):
            return 'X/Hybrid'
        return 'OPDK'

    def print_tree(startpath, prefix=''):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                print(f'{subindent}{f}')
            if level == 0:
                for d in dirs:
                    print_tree(os.path.join(root, d), prefix + '  ')
                break

    def detect_apigee_type_and_tree():
        import sys
        if len(sys.argv) != 2:
            print("Usage: python detect_apigee_type_and_tree.py <unzipped_api_bundle_dir>")
            sys.exit(1)
        bundle_path = sys.argv[1]
        apigee_type = detect_apigee_type(bundle_path)
        print(f"Detected Apigee API Proxy Type: {apigee_type}")
        print("File System Tree:")
        print_tree(bundle_path)

    if __name__ == "__main__":
        detect_apigee_type_and_tree()
