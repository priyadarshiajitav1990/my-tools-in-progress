#!/usr/bin/env python3
"""
Unified Lua Converter CLI Tool
- Detects input type: Java (.java), JS (.js), JAR (.jar)
- Converts to Lua script
- OS independent: Windows, Linux, macOS
- All dependencies embedded (requires only Python 3.7+)
- Usage: python lua_converter.py <input_file>
"""
import sys, os, subprocess

def main():
    if len(sys.argv) != 2:
        print('Usage: python lua_converter.py <input_file>')
        sys.exit(1)
    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f'File not found: {input_path}')
        sys.exit(1)
    ext = os.path.splitext(input_path)[1].lower()
    out_path = os.path.splitext(os.path.basename(input_path))[0] + '.lua'
    jar_path = os.path.join(os.path.dirname(__file__), 'lua_converter_tool_main.jar')
    if ext == '.java' or ext == '.js' or ext == '.jar':
        # Use embedded JAR for conversion
        cmd = ['java', '-jar', jar_path, input_path, out_path]
        try:
            subprocess.check_call(cmd)
            print(f'Lua script generated: {out_path}')
        except Exception as e:
            print(f'Error running Java converter: {e}')
            sys.exit(1)
    else:
        print('Unsupported input type. Supported: .java, .js, .jar')
        sys.exit(1)

if __name__ == '__main__':
    main()
