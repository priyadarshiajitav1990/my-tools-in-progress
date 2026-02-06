#!/usr/bin/env python3
"""
Standalone Python-to-Lua CLI Tool
- Converts any Python script (.py) to Lua script
- OS independent: Windows, Linux, macOS
- All dependencies embedded (requires only Python 3.7+)
- Usage: python py2lua_cli_standalone.py <input.py>
"""
import sys, os

# Ensure portable import of embedded modules
import importlib.util
module_dir = os.path.join(os.path.dirname(__file__), 'py_to_lua_modules')
sys.path.insert(0, module_dir)
PythonParser = importlib.import_module('parser').PythonParser
ASTTransformer = importlib.import_module('ast_transformer').ASTTransformer
LuaGenerator = importlib.import_module('lua_generator').LuaGenerator

def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.py'):
        print('Usage: python py2lua_cli_standalone.py <input.py>')
        sys.exit(1)
    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f'File not found: {input_path}')
        sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    parser = PythonParser()
    tree = parser.parse(source)
    generator = LuaGenerator()
    lua_code = generator.generate(tree)
    out_path = os.path.splitext(os.path.basename(input_path))[0] + '.lua'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(lua_code)
    print(f'Lua script generated: {out_path}')

if __name__ == '__main__':
    main()
