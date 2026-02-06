# Custom Plugin Usage Guide

This guide provides step-by-step instructions for using the following custom Kong plugins:
- jspolicy
- javapolicy
- kong-plugin-jspolicy
- pypolicy
- luafileexecuter

---

## 1. jspolicy

### 1. YAML Configuration Required
Define the plugin in your configuration as follows:
```yaml
plugins:
- name: jspolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"  # optional
    condition: "kong.request.get_method() == 'POST'"
    flow: "request"
    kv_pairs:
      user_role: "admin"
      max_limit: "100"
  tags:
    - custom
    - jspolicy
  ordering:
    before:
      - rate-limiting
    after:
      - key-auth
```

### 2. Where to Place Lua Scripts
- Place `main_policy.lua` and (optionally) `helper.lua` in:
  `/workspaces/my-tool-migrater020226/custom_plugins/jspolicy/`

### 3. Next Steps
- Ensure the plugin is enabled in Kong.
- Place your Lua scripts in the directory above.
- Reload or restart Kong to pick up new scripts.
- Test the plugin by making requests that match the configured condition.

---

## 2. javapolicy

### 1. YAML Configuration Required
```yaml
plugins:
- name: javapolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"  # optional
    condition: "ngx.var.request_method == 'GET'"
    flow: request
    kv_pairs:
      user_role: admin
      max_limit: "100"
  tags:
    - custom
    - policy
```

### 2. Where to Place Lua Scripts
- Place `main_policy.lua` and (optionally) `helper.lua` in:
  `/workspaces/my-tool-migrater020226/kong-plugin-javapolicy/kong/plugins/javapolicy/`

### 3. Next Steps
- Enable the plugin in Kong.
- Place your Lua scripts in the directory above.
- Reload or restart Kong.
- Test with requests matching the condition.

---

## 3. kong-plugin-jspolicy

### 1. YAML Configuration Required
```yaml
plugins:
- name: jspolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"  # optional
    condition: "ngx.var.request_method == 'GET'"
    flow: request
    kv_pairs:
      user_role: admin
      max_limit: "100"
  tags:
    - custom
    - policy
```

### 2. Where to Place Lua Scripts
- Place `main_policy.lua` and (optionally) `helper.lua` in:
  `/workspaces/my-tool-migrater020226/kong-plugin-jspolicy/kong/plugins/jspolicy/`

### 3. Next Steps
- Enable the plugin in Kong.
- Place your Lua scripts in the directory above.
- Reload or restart Kong.
- Test with requests matching the condition.

---

## 4. pypolicy

### 1. YAML Configuration Required
```yaml
plugins:
- name: pypolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"  # optional
    condition: "ngx.var.request_method == 'GET'"
    flow: request
    kv_pairs:
      user_role: admin
      max_limit: "100"
  tags:
    - custom
    - policy
```

### 2. Where to Place Lua Scripts
- Place `main_policy.lua` and (optionally) `helper.lua` in:
  `/workspaces/my-tool-migrater020226/kong-plugin-pypolicy/kong/plugins/pypolicy/`

### 3. Next Steps
- Enable the plugin in Kong.
- Place your Lua scripts in the directory above.
- Reload or restart Kong.
- Test with requests matching the condition.

---

## 5. luafileexecuter

### 1. YAML Configuration Required
```yaml
plugins:
- name: luafileexecuter
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"  # optional
    kv_pairs:
      user_role: admin
      max_limit: "100"
    tags:
      - custom
      - luafile
    ordering:
      before:
        - rate-limiting
      after:
        - key-auth
    flow: both
    condition: "kong.request.get_method() == 'POST'"
```

### 2. Where to Place Lua Scripts
- Place `main_policy.lua` and (optionally) `helper.lua` in:
  `/workspaces/my-tool-migrater020226/kong-custom-luafileexecuter/kong/plugins/luafileexecuter/`

### 3. Next Steps
- Enable the plugin in Kong.
- Place your Lua scripts in the directory above.
- Reload or restart Kong.
- Test with requests matching the condition.

---
