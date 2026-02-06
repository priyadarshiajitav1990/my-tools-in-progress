
import sys
import importlib
from pathlib import Path

def main():
	scripts_dir = Path(__file__).parent / 'scripts'
	sys.path.insert(0, str(scripts_dir))

	# Sequence of all scripts (grouped by logical steps)
	script_sequence = [
		# Config loading
		'config_loaded',
		'config-loaded',

		# Apigee bundle handling
		'list_apigee_zipfiles',
		'unzip_apigee_zipfiles',
		'apigee_bundle_xml2json',

		# API structure extraction
		'detect_apigee_type_and_tree',
		'extract_apigee_api_structure',

		# Endpoint conversion
		'proxyendpoint2service',
		'targetendpoint2service',

		# Resource handling
		'resources_files_handler',
		'resources_scripts_handler',
		'resources-files-handler',
		'resources-scripts-handler',

		# Policy to plugin conversion (all variants)
		'apigee_policy2acl',
		'apigee_policy2basic_auth',
		'apigee_policy2cors',
		'apigee_policy2file_log',
		'apigee_policy2hmac_auth',
		'apigee_policy2http_log',
		'apigee_policy2ip_restriction',
		'apigee_policy2jwt',
		'apigee_policy2key_auth',
		'apigee_policy2ldap_auth',
		'apigee_policy2oauth2',
		'apigee_policy2prometheus',
		'apigee_policy2proxy_cache_advanced',
		'apigee_policy2rate_limiting',
		'apigee_policy2rate_limiting_advanced',
		'apigee_policy2request_termination',
		'apigee_policy2request_transformer',
		'apigee_policy2request_validator',
		'apigee_policy2response_transformer',
		'apigee_policy2response_transformer_advanced',
		# Also call dash-variant scripts if needed
		'apigee-policy2acl',
		'apigee-policy2basic-auth',
		'apigee-policy2cors',
		'apigee-policy2file-log',
		'apigee-policy2hmac-auth',
		'apigee-policy2http-log',
		'apigee-policy2ip-restriction',
		'apigee-policy2jwt',
		'apigee-policy2key-auth',
		'apigee-policy2ldap-auth',
		'apigee-policy2oauth2',
		'apigee-policy2prometheus',
		'apigee-policy2proxy-cache-advanced',
		'apigee-policy2rate-limiting',
		'apigee-policy2rate-limiting-advanced',
		'apigee-policy2request-termination',
		'apigee-policy2request-transformer',
		'apigee-policy2request-validator',
		'apigee-policy2response-transformer',
		'apigee-policy2response-transformer-advanced',

		# Duplicate plugin logic
		'duplicate_plugin_handler',

		# Verification
		'verify_kong_output',

		# Deployment (add deployment script if present)
		'deploy_kong_config',

		# Report generation (add report script if present)
		'generate_report',

		# Utility/caller
		'caller_script',
	]

	for script in script_sequence:
		try:
			module = importlib.import_module(script)
		except Exception as e:
			print(f"Could not import {script}: {e}")
			continue
		if hasattr(module, 'main'):
			print(f"Running {script}.main()...")
			# Example condition: skip config-loaded if config_loaded succeeded
			if script == 'config-loaded' and 'config_loaded' in sys.modules:
				continue
			module.main()
		else:
			print(f"Script {script} does not have a main() function.")

if __name__ == "__main__":
	main()
