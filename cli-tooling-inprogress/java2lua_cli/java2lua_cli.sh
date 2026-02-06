#!/bin/bash
# Portable Java-to-Lua CLI Tool
# OS independent (Windows via Git Bash, Linux, macOS)
# Usage: ./java2lua_cli.sh <input.java>
# Output: <input>.lua in current directory

INPUT_FILE="$1"
if [ -z "$INPUT_FILE" ] || [[ "$INPUT_FILE" != *.java ]]; then
  echo "Usage: ./java2lua_cli.sh <input.java>"
  exit 1
fi
if [ ! -f "$INPUT_FILE" ]; then
  echo "File not found: $INPUT_FILE"
  exit 1
fi
JAR_PATH="$(dirname "$0")/lua_converter_tool_main.jar"
OUT_FILE="$(basename "$INPUT_FILE" .java).lua"
java -jar "$JAR_PATH" "$INPUT_FILE" "$OUT_FILE"
echo "Lua script generated: $OUT_FILE"
