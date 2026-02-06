#!/usr/bin/env python3
"""
List all zip files under APIGEE2KONGMIGRATIONTOOL/inputs
"""

import os

def get_zip_files(input_dir):
    zip_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_files.append(os.path.join(root, file))
    return zip_files

def print_zip_files(zip_files):
    for z in zip_files:
        print(z)

def list_apigee_zipfiles():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../inputs')
    zip_files = get_zip_files(input_dir)
    print_zip_files(zip_files)

if __name__ == "__main__":
    list_apigee_zipfiles()

def list_apigee_zipfiles():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../inputs')
    zip_files = get_zip_files(input_dir)
    print_zip_files(zip_files)

if __name__ == "__main__":
    list_apigee_zipfiles()
