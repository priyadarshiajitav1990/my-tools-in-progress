-- import: math (not directly supported in Lua)
-- class Foo
Foo = Foo or {}
Foo.__index = Foo
setmetatable(Foo, {__index = nil})
function Foo:new(o)
    o = o or {}
    setmetatable(o, self)
    return o
end
function __init__(self, x)
    self.x = x
end
    function bar(self, y)
    return -- list comprehension
local result = {}
for i in range(self.x) do
    table.insert(result, (i * y))
end
return result
end
-- async function baz not supported
function baz()
    -- await not supported: some_async_func()
end
function decorator(f)
    return f
end
test = decorator(test)
function test()
    -- try/except/finally not directly supported in Lua
print(Foo(5).bar(2))
-- except handler: print(e)


end