# Lua Converter CLI Tool

## Usage

```sh
./lua_converter.sh <input.java|input.js|input.jar>
```

- Converts Java, JS, or JAR files to Lua scripts.
- Output: `<input>.lua` in the current directory.

## Requirements
- Java 11+ (OpenJDK or Oracle)
- `lua_converter_tool_main.jar` in the same directory
- OS independent: Windows (Git Bash), Linux, macOS

## Migration Notice
- The old `java2lua_cli` is deprecated. Use `lua_converter.sh` for all conversions.
