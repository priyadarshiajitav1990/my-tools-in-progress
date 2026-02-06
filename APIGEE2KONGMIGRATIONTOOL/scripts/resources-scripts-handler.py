#!/usr/bin/env python3
"""
List all JavaScript, Java, JAR, and Python files in all resources directories of unzipped API bundles, with paths relative to APIGEE2KONGMIGRATIONTOOL.
"""
import os

def gather_resource_scripts(root_dir):
    script_exts = ['.js', '.java', '.jar', '.py']
    result = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if any(f.lower().endswith(ext) for ext in script_exts):
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
            scripts = gather_resource_scripts(resources_dir)
            print(f"Resources scripts in {bundle_name}:")
            for s in scripts:
                print(f"  {os.path.join('apigeeapiunzipped', bundle_name, 'apiproxy', 'resources', s)}")

if __name__ == "__main__":
    main()
