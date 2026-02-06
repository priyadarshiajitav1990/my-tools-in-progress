# Complex Python input for end-to-end CLI test
import math
class Foo:
    def __init__(self, x):
        self.x = x
    def bar(self, y):
        return [i*y for i in range(self.x)]
async def baz():
    await some_async_func()
def decorator(f):
    return f
@decorator
def test():
    try:
        print(Foo(5).bar(2))
    except Exception as e:
        print(e)
