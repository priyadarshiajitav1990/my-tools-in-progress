#!/usr/bin/env python3
"""
Unzip all zip files in APIGEE2KONGMIGRATIONTOOL/inputs to APIGEE2KONGMIGRATIONTOOL/apigeeapiunzipped/<zipfilename>/
"""

import os
import zipfile

def get_input_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../inputs')

def get_output_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../apigeeapiunzipped')

def unzip_file(zip_path, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    print(f"Unzipped {os.path.basename(zip_path)} to {dest_folder}")

def unzip_all_zip_files(input_dir, output_dir):
    for file in os.listdir(input_dir):
        if file.lower().endswith('.zip'):
            zip_path = os.path.join(input_dir, file)
            folder_name = os.path.splitext(file)[0]
            dest_folder = os.path.join(output_dir, folder_name)
            unzip_file(zip_path, dest_folder)

def unzip_apigee_zipfiles():
    input_dir = get_input_dir()
    output_dir = get_output_dir()
    unzip_all_zip_files(input_dir, output_dir)

if __name__ == "__main__":
    unzip_apigee_zipfiles()
