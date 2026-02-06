#!/usr/bin/env python3
"""
Portable Python-to-Lua CLI Tool
- OS independent (Windows, Linux, macOS)
- All dependencies embedded
- Usage: python py2lua_cli.py <input.py>
- Output: <input>.lua in current directory
"""
import sys, os
from py_to_lua.parser import PythonParser
from py_to_lua.ast_transformer import ASTTransformer
from py_to_lua.lua_generator import LuaGenerator

def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.py'):
        print('Usage: python py2lua_cli.py <input.py>')
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
