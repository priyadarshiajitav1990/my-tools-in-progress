"""
Lua code generator for Python-to-Lua converter.
"""
from typing import Any
import ast

class LuaGenerator:
	def visit_Nonlocal(self, node: ast.Nonlocal) -> str:
		return f'-- nonlocal {", ".join(node.names)} (not supported in Lua)'

	def visit_Global(self, node: ast.Global) -> str:
		return f'-- global {", ".join(node.names)} (not supported in Lua)'

	def visit_Pass(self, node: ast.Pass) -> str:
		return '-- pass'

	def visit_Break(self, node: ast.Break) -> str:
		return 'break'

	def visit_Continue(self, node: ast.Continue) -> str:
		return 'continue'

	def visit_Raise(self, node: ast.Raise) -> str:
		if node.exc:
			return f'error({self.visit(node.exc)})'
		return 'error()'

	def visit_Assert(self, node: ast.Assert) -> str:
		if node.msg:
			return f'assert({self.visit(node.test)}, {self.visit(node.msg)})'
		return f'assert({self.visit(node.test)})'

	def visit_Starred(self, node: ast.Starred) -> str:
		return f'-- starred: {self.visit(node.value)} (not supported in Lua)'

	def visit_Import(self, node: ast.Import) -> str:
		imports = ', '.join(alias.name for alias in node.names)
		return f'-- import: {imports} (not directly supported in Lua)'

	def visit_ImportFrom(self, node: ast.ImportFrom) -> str:
		module = node.module or ''
		names = ', '.join(alias.name for alias in node.names)
		return f'-- from {module} import {names} (not directly supported in Lua)'

	def visit_Attribute(self, node: ast.Attribute) -> str:
		value = self.visit(node.value)
		return f'{value}.{node.attr}'

	def visit_Call(self, node: ast.Call) -> str:
		func_str = self.visit(node.func)
		is_requests_call = False
		method = None
		if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'requests':
			is_requests_call = True
			method = node.func.attr
		elif func_str.startswith('requests.'):
			is_requests_call = True
			method = func_str.split('.')[-1]
		if is_requests_call and method:
			url = self.visit(node.args[0]) if node.args else 'URL'
			if method == 'get':
				return f'-- HTTP GET request\nlocal res = http.request({url})'
			elif method == 'post':
				return f'-- HTTP POST request\nlocal res = http.request({url}, "POST", ...)'  # Simplified
			else:
				return f'-- HTTP {method.upper()} request\nlocal res = http.request({url}, "{method.upper()}", ...)'  # Simplified
		if func_str in ('app.route', 'app.get', 'app.post', 'app.put', 'app.delete'):
			return f'-- REST API route handler ({func_str})'
		args = ', '.join(self.visit(arg) for arg in node.args)
		return f'{func_str}({args})'
	def visit_Lambda(self, node: ast.Lambda) -> str:
		args = ', '.join(node.args.args[i].arg if hasattr(node.args.args[i], 'arg') else str(node.args.args[i]) for i in range(len(node.args.args)))
		body = self.visit(node.body)
		return f'function({args}) return {body} end'

	def visit_ListComp(self, node: ast.ListComp) -> str:
		elt = self.visit(node.elt)
		gen = node.generators[0]
		target = self.visit(gen.target)
		iter_ = self.visit(gen.iter)
		code = f'local result = {{}}\nfor {target} in {iter_} do\n    table.insert(result, {elt})\nend\nreturn result'
		return f'-- list comprehension\n{code}'

	def visit_DictComp(self, node: ast.DictComp) -> str:
		key = self.visit(node.key)
		value = self.visit(node.value)
		gen = node.generators[0]
		target = self.visit(gen.target)
		iter_ = self.visit(gen.iter)
		code = f'local result = {{}}\nfor {target} in {iter_} do\n    result[{key}] = {value}\nend\nreturn result'
		return f'-- dict comprehension\n{code}'

	def visit_comprehension(self, node: ast.comprehension) -> str:
		return self.visit(node.iter)

	def visit_With(self, node: ast.With) -> str:
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		return f'-- with statement emulation (context manager)\nlocal _ok, _err = pcall(function()\n    {body}\nend)\nif not _ok then\n    -- handle context manager exit/cleanup here\nend'

	def visit_Try(self, node: ast.Try) -> str:
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		handlers = '\n'.join(self.visit(h) for h in node.handlers)
		orelse = '\n    '.join(self.visit(stmt) for stmt in node.orelse)
		finalbody = '\n    '.join(self.visit(stmt) for stmt in node.finalbody)
		return f'-- try/except/finally not directly supported in Lua\n{body}\n{handlers}\n{orelse}\n{finalbody}'

	def visit_ExceptHandler(self, node: ast.ExceptHandler) -> str:
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		return f'-- except handler: {body}'

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> str:
		return f'-- async function {node.name} not supported\n' + self.visit_FunctionDef(node)

	def visit_Await(self, node: ast.Await) -> str:
		return f'-- await not supported: {self.visit(node.value)}'

	def visit_AsyncFor(self, node: ast.AsyncFor) -> str:
		return f'-- async for not supported\n' + self.visit_For(node)

	def visit_AsyncWith(self, node: ast.AsyncWith) -> str:
		return f'-- async with not supported\n' + self.visit_With(node)

	def visit_Yield(self, node: ast.Yield) -> str:
		if node.value:
			return f'coroutine.yield({self.visit(node.value)})'
		return 'coroutine.yield()'

	def visit_YieldFrom(self, node: ast.YieldFrom) -> str:
		return f'-- yield from emulation: {self.visit(node.value)}'

	def visit_Decorator(self, node) -> str:
		return f'-- decorator emulation: {self.visit(node)}'

	def visit_FunctionDef(self, node: ast.FunctionDef) -> str:
		args = ', '.join(arg.arg for arg in node.args.args)
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		func_code = f'function {node.name}({args})\n    {body}\nend'
		if hasattr(node, 'decorator_list') and node.decorator_list:
			for deco in reversed(node.decorator_list):
				deco_str = self.visit(deco)
				func_code = f'{node.name} = {deco_str}({node.name})\n' + func_code
		return func_code
	def generate(self, node: ast.AST) -> str:
		return self.visit(node)

	def visit(self, node):
		method = 'visit_' + type(node).__name__
		visitor = getattr(self, method, self.generic_visit)
		return visitor(node)

	def visit_Module(self, node: ast.Module) -> str:
		return '\n'.join(self.visit(stmt) for stmt in node.body)

	def visit_Expr(self, node: ast.Expr) -> str:
		return self.visit(node.value)

	def visit_Assign(self, node: ast.Assign) -> str:
		targets = [self.visit(t) for t in node.targets]
		value = self.visit(node.value)
		return f'{" = ".join(targets)} = {value}'

	def visit_Name(self, node: ast.Name) -> str:
		return node.id

	def visit_BinOp(self, node: ast.BinOp) -> str:
		left = self.visit(node.left)
		right = self.visit(node.right)
		op = self.visit(node.op)
		return f'({left} {op} {right})'

	def visit_Add(self, node: ast.Add) -> str:
		return '+'

	def visit_Sub(self, node: ast.Sub) -> str:
		return '-'

	def visit_Mult(self, node: ast.Mult) -> str:
		return '*'

	def visit_Div(self, node: ast.Div) -> str:
		return '/'

	def visit_If(self, node: ast.If) -> str:
		test = self.visit(node.test)
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		orelse = ''
		if node.orelse:
			orelse = '\nelse\n    ' + '\n    '.join(self.visit(stmt) for stmt in node.orelse)
		return f'if {test} then\n    {body}{orelse}\nend'

	def visit_Compare(self, node: ast.Compare) -> str:
		left = self.visit(node.left)
		ops = ' '.join(self.visit(op) for op in node.ops)
		comparators = ' '.join(self.visit(comp) for comp in node.comparators)
		return f'{left} {ops} {comparators}'

	def visit_Eq(self, node: ast.Eq) -> str:
		return '=='

	def visit_NotEq(self, node: ast.NotEq) -> str:
		return '~='

	def visit_Lt(self, node: ast.Lt) -> str:
		return '<'

	def visit_LtE(self, node: ast.LtE) -> str:
		return '<='

	def visit_Gt(self, node: ast.Gt) -> str:
		return '>'

	def visit_GtE(self, node: ast.GtE) -> str:
		return '>='

	def visit_For(self, node: ast.For) -> str:
		target = self.visit(node.target)
		iter_ = self.visit(node.iter)
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		return f'for {target} in {iter_} do\n    {body}\nend'

	def visit_While(self, node: ast.While) -> str:
		test = self.visit(node.test)
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		return f'while {test} do\n    {body}\nend'

	def visit_List(self, node: ast.List) -> str:
		elts = ', '.join(self.visit(e) for e in node.elts)
		return f'{{{elts}}}'

	def visit_Dict(self, node: ast.Dict) -> str:
		items = ', '.join(f'[{self.visit(k)}]={self.visit(v)}' for k, v in zip(node.keys, node.values))
		return f'{{{items}}}'

	def visit_Return(self, node: ast.Return) -> str:
		if node.value:
			return f'return {self.visit(node.value)}'
		return 'return'

	def visit_ClassDef(self, node: ast.ClassDef) -> str:
		class_name = node.name
		bases = [self.visit(b) for b in node.bases] if hasattr(node, 'bases') else []
		base = bases[0] if bases else 'nil'
		body = '\n    '.join(self.visit(stmt) for stmt in node.body)
		return (f'-- class {class_name}\n'
				f'{class_name} = {class_name} or {{}}\n'
				f'{class_name}.__index = {class_name}\n'
				f'setmetatable({class_name}, {{__index = {base}}})\n'
				f'function {class_name}:new(o)\n'
				f'    o = o or {{}}\n'
				f'    setmetatable(o, self)\n'
				f'    return o\n'
				f'end\n'
				f'{body}')

	def visit_Constant(self, node: ast.Constant) -> str:
		if isinstance(node.value, str):
			return f'"{node.value}"'
		return str(node.value)

	def generic_visit(self, node):
		return f'-- Unhandled node: {type(node).__name__}'
