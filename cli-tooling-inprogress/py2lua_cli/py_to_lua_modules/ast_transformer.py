"""
AST Transformer to convert Python AST to an intermediate representation suitable for Lua code generation.
"""
import ast
from typing import Any

class ASTTransformer(ast.NodeVisitor):
	def visit_Nonlocal(self, node: ast.Nonlocal):
		return {'type': 'Nonlocal', 'names': node.names}

	def visit_Global(self, node: ast.Global):
		return {'type': 'Global', 'names': node.names}

	def visit_Pass(self, node: ast.Pass):
		return {'type': 'Pass'}

	def visit_Break(self, node: ast.Break):
		return {'type': 'Break'}

	def visit_Continue(self, node: ast.Continue):
		return {'type': 'Continue'}

	def visit_Raise(self, node: ast.Raise):
		return {'type': 'Raise', 'exc': self.visit(node.exc) if node.exc else None, 'cause': self.visit(node.cause) if node.cause else None}

	def visit_Assert(self, node: ast.Assert):
		return {'type': 'Assert', 'test': self.visit(node.test), 'msg': self.visit(node.msg) if node.msg else None}

	def visit_Starred(self, node: ast.Starred):
		return {'type': 'Starred', 'value': self.visit(node.value)}
	def visit_Import(self, node: ast.Import):
		return {
			'type': 'Import',
			'names': [alias.name for alias in node.names],
			'asnames': [alias.asname for alias in node.names],
		}

	def visit_ImportFrom(self, node: ast.ImportFrom):
		return {
			'type': 'ImportFrom',
			'module': node.module,
			'names': [alias.name for alias in node.names],
			'asnames': [alias.asname for alias in node.names],
			'level': node.level,
		}

	def visit_Attribute(self, node: ast.Attribute):
		return {
			'type': 'Attribute',
			'value': self.visit(node.value),
			'attr': node.attr,
		}

	def visit_Call(self, node: ast.Call):
		func = self.visit(node.func)
		args = [self.visit(arg) for arg in node.args]
		keywords = [self.visit(kw) for kw in node.keywords]
		return {
			'type': 'Call',
			'func': func,
			'args': args,
			'keywords': keywords,
		}
