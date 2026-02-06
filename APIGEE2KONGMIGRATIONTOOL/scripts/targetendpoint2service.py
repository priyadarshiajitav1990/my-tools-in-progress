"""
Enterprise-grade script to convert Apigee TargetEndpoint XML to Kong service YAML using a Jinja template.
- Each function is modular and documented.
- Mandatory and optional fields are clearly marked.
- Usage: python targetendpoint2service.py <targetendpoint.xml> <output.yaml>
"""
import sys
import os
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader

def parse_target_endpoint(xml_path):
    """
    Parse Apigee TargetEndpoint XML and extract relevant info for Kong service.
    Args:
        xml_path (str): Path to Apigee TargetEndpoint XML file. (MANDATORY)
    Returns:
        dict: Extracted service info (MANDATORY/OPTIONAL fields as per template)
    Raises:
        Exception: If mandatory fields are missing or XML is invalid.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    name = root.attrib.get('name')
    if not name:
        raise Exception('TargetEndpoint must have a name attribute (MANDATORY)')
    services = []
    import urllib.parse
    for idx, http in enumerate(root.findall('.//HTTPTargetConnection')):
        # Defaults
        url = None
        protocol = 'http'
        host = None
        port = 80
        path = '/'
        url_elem = http.find('URL')
        if url_elem is not None and url_elem.text:
            url = url_elem.text.strip()
        host_elem = http.find('Host')
        if host_elem is not None and host_elem.text:
            host = host_elem.text.strip()
        port_elem = http.find('Port')
        if port_elem is not None and port_elem.text:
            port = int(port_elem.text.strip())
        ssl_elem = http.find('SSLInfo')
        if ssl_elem is not None:
            protocol = 'https'
        path_elem = http.find('BasePath')
        if path_elem is not None and path_elem.text:
            path = path_elem.text.strip()
        # If URL is present, parse it for host/port/path/protocol
        if url:
            parsed = urllib.parse.urlparse(url)
            protocol = parsed.scheme or protocol
            host = parsed.hostname or host
            port = parsed.port or port
            path = parsed.path or path
        if not host:
            raise Exception(f'HTTPTargetConnection #{idx+1} must have a host (MANDATORY)')
        # OPTIONAL: Timeouts, retries, tags
        retries = 5
        connect_timeout = 60000
        write_timeout = 60000
        read_timeout = 60000
        tags = ['apigee-migrated']
        service_name = name if len(root.findall('.//HTTPTargetConnection')) == 1 else f"{name}_{idx+1}"
        services.append({
            'name': service_name,
            'url': url or f"{protocol}://{host}:{port}{path}",
            'protocol': protocol,
            'host': host,
            'port': port,
            'path': path,
            'retries': retries,
            'connect_timeout': connect_timeout,
            'write_timeout': write_timeout,
            'read_timeout': read_timeout,
            'tags': tags
        })
    return services

def render_kong_service(service_info, template_dir, output_path):
    """
    Render the Kong service YAML using the Jinja template and extracted info.
    Args:
        service_info (dict): Service info from parse_target_endpoint (MANDATORY)
        template_dir (str): Directory containing Jinja template (MANDATORY)
        output_path (str): Output YAML file path (MANDATORY)
    """
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('kong_service.j2')
    with open(output_path, 'w') as f:
        for idx, service in enumerate(service_info):
            rendered = template.render(**service)
            f.write(rendered)
            if idx < len(service_info) - 1:
                f.write('\n---\n')
    print(f"Kong service YAML(s) written to {output_path}")

def main():
    """
    Main execution: parse args, call parse and render functions in sequence.
    """
    if len(sys.argv) != 3:
        print("Usage: python targetendpoint2service.py <targetendpoint.xml> <output.yaml>")
        sys.exit(1)
    xml_path = sys.argv[1]
    output_path = sys.argv[2]
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
    services = parse_target_endpoint(xml_path)
    render_kong_service(services, template_dir, output_path)

if __name__ == "__main__":
    main()
