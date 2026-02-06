"""
Python source code parser for Python-to-Lua converter.
"""
import ast
from typing import Any

class PythonParser:
	def parse(self, source: str) -> ast.AST:
		"""Parse Python source code into an AST."""
		return ast.parse(source)
