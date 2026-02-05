import re
import sys
import os

# Mapping: Apigee pattern (as regex) -> Kong replacement (with group references)
PATTERNS = [
    # 1. context.getVariable('X') or context.getVariable("X") or context.getVariable(X)
    (r'context\.getVariable\s*\(\s*([\'"])(.*?)\1\s*\)', r'kong.request.get_query_arg("\2")'), # literal string
    (r'context\.getVariable\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)', r'kong.request.get_query_arg(\1)'), # variable

    # 2. context.setVariable('X', value) or context.setVariable("X", value) or context.setVariable(X, value)
    (r'context\.setVariable\s*\(\s*([\'"])(.*?)\1\s*,\s*([^)]+)\)', r'kong.service.request.set_header("\2", \3)'), # literal string
    (r'context\.setVariable\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*,\s*([^)]+)\)', r'kong.service.request.set_header(\1, \2)'), # variable

    # 3. request.headers['X'] or request.headers["X"] or request.headers[X]
    (r'request\.headers\s*\[\s*([\'"])(.*?)\1\s*\]', r'kong.request.get_header("\2")'), # literal string
    (r'request\.headers\s*\[\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\]', r'kong.request.get_header(\1)'), # variable

    # 4. response.headers['X'] or response.headers["X"] or response.headers[X]
    (r'response\.headers\s*\[\s*([\'"])(.*?)\1\s*\]', r'kong.response.get_header("\2")'), # literal string
    (r'response\.headers\s*\[\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\]', r'kong.response.get_header(\1)'), # variable

    # 5. request.content()
    (r'request\.content\s*\(\s*\)', r'kong.request.get_raw_body()'),

    # 6. response.content = value
    (r'response\.content\s*=\s*([^\n]+)', r'kong.response.set_raw_body(\1)'),

    # 7. print(
    (r'\bprint\s*\(', r'kong.log.inspect('),

    # 8. throw(
    (r'\bthrow\s*\(', r'error('),
]

def apigee_to_kong_lua(lua_code):
    for pat, repl in PATTERNS:
        lua_code = re.sub(pat, repl, lua_code)
    return lua_code

def process_file(input_file, output_file=None):
    with open(input_file, "r", encoding="utf-8") as f:
        lua_code = f.read()
    converted = apigee_to_kong_lua(lua_code)
    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_kong{ext}"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(converted)
    print(f"Converted file written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python apigee_to_kong_var_replacer.py <input_lua_file> [output_lua_file]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    process_file(input_file, output_file)