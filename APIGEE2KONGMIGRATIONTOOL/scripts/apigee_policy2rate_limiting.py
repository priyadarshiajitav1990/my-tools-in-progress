"""
Enterprise_grade script to convert Apigee SpikeArrest/Quota policy to Kong rate_limiting plugin YAML using Jinja template and policy2plugin.json mapping.
_ Modular functions, clear comments, mandatory/optional fields.
_ Usage: python apigee_policy2rate_limiting.py <policy.xml> <service_name> <output.yaml>
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

def parse_spikearrest_quota_policy(xml_path):
    """
    Parse Apigee SpikeArrest/Quota XML and extract config for rate_limiting plugin.
    Args:
        xml_path (str): Path to Apigee policy XML file. (MANDATORY)
    Returns:
        dict: Plugin config (MANDATORY/OPTIONAL fields)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    config = {}
    # Example: <Rate>100pm</Rate> or <Interval>1</Interval> <TimeUnit>minute</TimeUnit>
    rate_elem = root.find('Rate')
    if rate_elem is not None and rate_elem.text:
        import re
        match = re.match(r'(\d+)([a_z]+)', rate_elem.text.strip())
        if match:
            value, unit = match.groups()
            config[unit] = int(value)
    interval_elem = root.find('Interval')
    timeunit_elem = root.find('TimeUnit')
    if interval_elem is not None and timeunit_elem is not None:
        config[timeunit_elem.text.strip()] = int(interval_elem.text.strip())
    # Policy type
    config['policy'] = 'local'
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
        'tags': ['apigee_migrated']
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
        print("Usage: python apigee_policy2rate_limiting.py <policy.xml> <service_name> <output.yaml>")
        sys.exit(1)
    xml_path = sys.argv[1]
    service_name = sys.argv[2]
    output_path = sys.argv[3]
    mapper_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mappers/policy2plugin.json')
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    mapper = load_policy2plugin_mapper(mapper_path)
    # Determine plugin type from XML root tag
    tree = ET.parse(xml_path)
    root = tree.getroot()
    apigee_policy_type = root.tag
    kong_plugin = mapper.get(apigee_policy_type, 'rate_limiting')
    config = parse_spikearrest_quota_policy(xml_path)
    render_plugin(kong_plugin, config, service_name, template_dir, output_path)

if __name__ == "__main__":
    main()
