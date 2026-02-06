#!/usr/bin/env python3
"""
Caller script to run all main functions of the tool scripts in the required sequence.
"""
import sys
import os

def run_config_loaded():
    from config_loaded import config_loaded
    config_loaded()

def run_list_apigee_zipfiles():
    from list_apigee_zipfiles import list_apigee_zipfiles
    list_apigee_zipfiles()

def run_unzip_apigee_zipfiles():
    from unzip_apigee_zipfiles import unzip_apigee_zipfiles
    unzip_apigee_zipfiles()

def run_detect_apigee_type_and_tree(bundle_dir):
    from detect_apigee_type_and_tree import detect_apigee_type_and_tree
    sys.argv = ['detect_apigee_type_and_tree.py', bundle_dir]
    detect_apigee_type_and_tree()

def run_apigee_bundle_xml2json(bundle_dir):
    from apigee_bundle_xml2json import apigee_bundle_xml2json
    sys.argv = ['apigee_bundle_xml2json.py', bundle_dir]
    apigee_bundle_xml2json()

def caller_script():
    run_config_loaded()
    run_list_apigee_zipfiles()
    run_unzip_apigee_zipfiles()
    # Iterate over unzipped bundles and run next steps
    unzipped_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../apigeeapiunzipped')
    for bundle_name in os.listdir(unzipped_dir):
        bundle_dir = os.path.join(unzipped_dir, bundle_name)
        if os.path.isdir(bundle_dir):
            run_detect_apigee_type_and_tree(bundle_dir)
            run_apigee_bundle_xml2json(bundle_dir)

if __name__ == "__main__":
    caller_script()
