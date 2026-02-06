#!/bin/bash
# Portable Lua Converter CLI Tool
# Supports: Java, JS, JAR
# OS independent (Windows via Git Bash, Linux, macOS)
# Usage: ./lua_converter.sh <input.java|input.js|input.jar>
# Output: <input>.lua in current directory

INPUT_FILE="$1"
if [ -z "$INPUT_FILE" ]; then
  echo "Usage: ./lua_converter.sh <input.java|input.js|input.jar>"
  exit 1
fi
if [ ! -f "$INPUT_FILE" ]; then
  echo "File not found: $INPUT_FILE"
  exit 1
fi
JAR_PATH="$(dirname "$0")/lua_converter_tool_main.jar"
OUT_FILE="$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//').lua"
java -jar "$JAR_PATH" "$INPUT_FILE" "$OUT_FILE"
echo "Lua script generated: $OUT_FILE"
