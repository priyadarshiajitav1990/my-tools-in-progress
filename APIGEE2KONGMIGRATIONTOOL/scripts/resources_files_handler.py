#!/usr/bin/env python3
"""
List all .xsl, .yaml, .yml, .json, .wsdl and other non_script files in all resources directories of unzipped API bundles, with paths relative to APIGEE2KONGMIGRATIONTOOL.
"""
import os

def gather_resource_files(root_dir):
    file_exts = ['.xsl', '.yaml', '.yml', '.json', '.wsdl']
    script_exts = ['.js', '.java', '.jar', '.py']
    result = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in file_exts or (ext not in script_exts and ext):
                rel_path = os.path.relpath(os.path.join(dirpath, f), root_dir)
                result.append(rel_path)
    return result

def main():
    apigee_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    unzipped_dir = os.path.join(apigee_root, 'apigeeapiunzipped')
    for bundle_name in os.listdir(unzipped_dir):
        bundle_dir = os.path.join(unzipped_dir, bundle_name)
        resources_dir = os.path.join(bundle_dir, 'apiproxy', 'resources')
        if os.path.isdir(resources_dir):
            files = gather_resource_files(resources_dir)
            print(f"Resources files in {bundle_name}:")
            for s in files:
                print(f"  {os.path.join('apigeeapiunzipped', bundle_name, 'apiproxy', 'resources', s)}")

if __name__ == "__main__":
    main()
