import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
	base_dir = Path(__file__).resolve().parent.parent
	venv_dir = base_dir / 'venv'
	requirements = base_dir / 'setups' / 'requirements.txt'

	# Detect OS type
	os_type = platform.system().lower()
	print(f"Detected OS: {os_type}")

	# Create virtual environment
	if not venv_dir.exists():
		print(f"Creating virtual environment at {venv_dir}")
		subprocess.check_call([sys.executable, '-m', 'venv', str(venv_dir)])
	else:
		print(f"Virtual environment already exists at {venv_dir}")

	# Activate virtual environment and install requirements
	if os_type == 'windows':
		activate_script = venv_dir / 'Scripts' / 'activate'
		python_bin = venv_dir / 'Scripts' / 'python.exe'
		pip_bin = venv_dir / 'Scripts' / 'pip.exe'
	else:
		activate_script = venv_dir / 'bin' / 'activate'
		python_bin = venv_dir / 'bin' / 'python'
		pip_bin = venv_dir / 'bin' / 'pip'

	print(f"Installing requirements from {requirements}")
	subprocess.check_call([str(pip_bin), 'install', '-r', str(requirements)])

	print("Setup complete. To activate the virtual environment, run:")
	print(f"source {activate_script}")

if __name__ == "__main__":
	main()
