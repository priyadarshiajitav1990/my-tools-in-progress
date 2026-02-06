"""
Enterprise-grade script to convert Apigee CORS policy to Kong cors plugin YAML using Jinja template and policy2plugin.json mapping.
- Modular functions, clear comments, mandatory/optional fields.
- Usage: python apigee-policy2cors.py <policy.xml> <service_name> <output.yaml>
"""
import sys
import os
import json
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

def load_policy2plugin_mapper(mapper_path):
    """
    Load Apigee policy to Kong plugin mapping from JSON file. (MANDATORY)
    """
    with open(mapper_path) as f:
        return json.load(f)

def parse_cors_policy(xml_path):
    """
    Parse Apigee CORS policy XML and extract config for cors plugin.
    Args:
        xml_path (str): Path to Apigee policy XML file. (MANDATORY)
    Returns:
        dict: Plugin config (MANDATORY/OPTIONAL fields)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    config = {
        'origins': [],
        'methods': [],
        'headers': [],
        'exposed_headers': [],
        'credentials': False,
        'max_age': 0
    }
    origins_elem = root.find('AllowedOrigins')
    if origins_elem is not None:
        for o in origins_elem.findall('Origin'):
            if o.text:
                config['origins'].append(o.text.strip())
    methods_elem = root.find('AllowedMethods')
    if methods_elem is not None:
        for m in methods_elem.findall('Method'):
            if m.text:
                config['methods'].append(m.text.strip())
    headers_elem = root.find('AllowedHeaders')
    if headers_elem is not None:
        for h in headers_elem.findall('Header'):
            if h.text:
                config['headers'].append(h.text.strip())
    exposed_elem = root.find('ExposedHeaders')
    if exposed_elem is not None:
        for h in exposed_elem.findall('Header'):
            if h.text:
                config['exposed_headers'].append(h.text.strip())
    cred_elem = root.find('AllowCredentials')
    if cred_elem is not None and cred_elem.text:
        config['credentials'] = cred_elem.text.strip().lower() == 'true'
    maxage_elem = root.find('MaxAge')
    if maxage_elem is not None and maxage_elem.text:
        config['max_age'] = int(maxage_elem.text.strip())
    return config

def render_plugin(plugin_name, config, service_name, template_dir, output_path):
    """
    Render Kong plugin YAML using Jinja template and extracted config.
    Args:
        plugin_name (str): Kong plugin name (MANDATORY)
        config (dict): Plugin config (MANDATORY)
        service_name (str): Associated Kong service name (MANDATORY)
        template_dir (str): Directory containing Jinja template (MANDATORY)
        output_path (str): Output YAML file path (MANDATORY)
    """
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(f'{plugin_name}.j2')
    plugin_info = {
        'name': plugin_name,
        'service': service_name,
        'config': config,
        'enabled': True,
        'protocols': ['http', 'https'],
        'tags': ['apigee-migrated']
    }
    rendered = template.render(**plugin_info)
    with open(output_path, 'w') as f:
        f.write(rendered)
    print(f"Kong plugin YAML written to {output_path}")

def main():
    """
    Main execution: parse args, load mapper, call parse and render functions in sequence.
    """
    if len(sys.argv) != 4:
        print("Usage: python apigee-policy2cors.py <policy.xml> <service_name> <output.yaml>")
        sys.exit(1)
    xml_path = sys.argv[1]
    service_name = sys.argv[2]
    output_path = sys.argv[3]
    mapper_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mappers/policy2plugin.json')
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    mapper = load_policy2plugin_mapper(mapper_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    apigee_policy_type = root.tag
    kong_plugin = mapper.get(apigee_policy_type, 'cors')
    config = parse_cors_policy(xml_path)
    render_plugin(kong_plugin, config, service_name, template_dir, output_path)

if __name__ == "__main__":
    main()
