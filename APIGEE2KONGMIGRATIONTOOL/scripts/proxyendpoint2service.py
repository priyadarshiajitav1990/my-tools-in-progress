"""
Enterprise-grade script to convert Apigee ProxyEndpoint XML to Kong route YAML using a Jinja template.
- Each function is modular and documented.
- Mandatory and optional fields are clearly marked.
- Usage: python proxyendpoint2service.py <proxyendpoint.xml> <service_name> <output.yaml>
"""
import sys
import os
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

def parse_proxy_endpoint(xml_path):
    """
    Parse Apigee ProxyEndpoint XML and extract route info for Kong.
    Args:
        xml_path (str): Path to Apigee ProxyEndpoint XML file. (MANDATORY)
    Returns:
        list[dict]: List of route info dicts (MANDATORY/OPTIONAL fields as per template)
    Raises:
        Exception: If mandatory fields are missing or XML is invalid.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # MANDATORY: Extract name
    name = root.attrib.get('name')
    if not name:
        raise Exception('ProxyEndpoint must have a name attribute (MANDATORY)')
    # MANDATORY: Extract basePath(s)
    base_paths = []
    for preflow in root.findall('.//BasePath'):
        if preflow.text:
            base_paths.append(preflow.text.strip())
    if not base_paths:
        raise Exception('ProxyEndpoint must have at least one BasePath (MANDATORY)')
    # OPTIONAL: Extract allowed HTTP methods from Condition or Flows
    methods = set()
    for flow in root.findall('.//Flow'):
        cond = flow.find('Condition')
        if cond is not None and cond.text:
            import re
            # Example: (request.verb == "GET" or request.verb == "POST")
            found = re.findall(r'request.verb\s*==\s*"(\w+)"', cond.text)
            methods.update(found)
    if not methods:
        methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"} # Default: all
    # OPTIONAL: Extract path conditions (for conditional flows)
    paths = set(base_paths)
    for flow in root.findall('.//Flow'):
        cond = flow.find('Condition')
        if cond is not None and cond.text:
            import re
            # Example: proxy.pathsuffix MatchesPath "/foo/bar"
            found = re.findall(r'proxy.pathsuffix\s*MatchesPath\s*"([^"]+)"', cond.text)
            for p in found:
                for bp in base_paths:
                    paths.add(bp.rstrip('/') + p)
    # MANDATORY: Service name must be provided as argument
    return [{
        'name': name,
        'service': None,  # To be filled in main()
        'paths': list(paths),
        'methods': list(methods),
        'strip_path': True,
        'preserve_host': False,
        'protocols': ["http", "https"],
        'hosts': [],
        'regex_priority': 0,
        'tags': ['apigee-migrated']
    }]

def render_kong_routes(routes, service_name, template_dir, output_path):
    """
    Render Kong route YAML(s) using the Jinja template and extracted info.
    Args:
        routes (list[dict]): Route info dicts from parse_proxy_endpoint (MANDATORY)
        service_name (str): Associated Kong service name (MANDATORY)
        template_dir (str): Directory containing Jinja template (MANDATORY)
        output_path (str): Output YAML file path (MANDATORY)
    """
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('kong_route.j2')
    with open(output_path, 'w') as f:
        for route in routes:
            route['service'] = service_name
            rendered = template.render(**route)
            f.write(rendered + '\n---\n')
    print(f"Kong route YAML(s) written to {output_path}")

def main():
    """
    Main execution: parse args, call parse and render functions in sequence.
    """
    if len(sys.argv) != 4:
        print("Usage: python proxyendpoint2service.py <proxyendpoint.xml> <service_name> <output.yaml>")
        sys.exit(1)
    xml_path = sys.argv[1]
    service_name = sys.argv[2]
    output_path = sys.argv[3]
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    routes = parse_proxy_endpoint(xml_path)
    render_kong_routes(routes, service_name, template_dir, output_path)

if __name__ == "__main__":
    main()
