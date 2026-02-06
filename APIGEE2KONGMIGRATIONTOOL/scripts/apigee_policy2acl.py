"""
Enterprise_grade script to convert Apigee AccessEntity policy to Kong acl plugin YAML using Jinja template and policy2plugin.json mapping.
_ Modular functions, clear comments, mandatory/optional fields.
_ Usage: python apigee_policy2acl.py <policy.xml> <output.yaml>
"""
import sys
import os
import json
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

def load_policy2plugin_mapper(mapper_path):
    with open(mapper_path) as f:
        return json.load(f)

def parse_accessentity_policy(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    config = {'allow': [], 'deny': []}
    for allow in root.findall('Allow'):
        if allow.text:
            config['allow'].append(allow.text.strip())
    for deny in root.findall('Deny'):
        if deny.text:
            config['deny'].append(deny.text.strip())
    return config

def render_plugin(plugin_name, config, template_dir, output_path):
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(f'{plugin_name}.j2')
    plugin_info = {'name': plugin_name, 'config': config}
    rendered = template.render(**plugin_info)
    with open(output_path, 'w') as f:
        f.write(rendered)
    print(f"Kong plugin YAML written to {output_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python apigee_policy2acl.py <policy.xml> <output.yaml>")
        sys.exit(1)
    xml_path = sys.argv[1]
    output_path = sys.argv[2]
    mapper_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mappers/policy2plugin.json')
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    mapper = load_policy2plugin_mapper(mapper_path)
    plugin_name = 'acl'
    config = parse_accessentity_policy(xml_path)
    render_plugin(plugin_name, config, template_dir, output_path)

if __name__ == "__main__":
    main()
