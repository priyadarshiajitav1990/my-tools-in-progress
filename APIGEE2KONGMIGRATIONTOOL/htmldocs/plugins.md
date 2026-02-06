# Kong Custom Plugins Reference


This document provides a comprehensive reference for all custom plugins in this workspace, including configuration, parameters, script search paths, and Jinja templates.

---

## Lua Script File Directories for Plugins

The following plugins require the Lua scripts referenced by `script_name` and `dependency_name` to be present in the specified directory:

| Plugin                | Full Lua Scripts Directory Path                                                                 |
|-----------------------|-----------------------------------------------------------------------------------------------|
| jspolicy              | /workspaces/my-tool-migrater020226/custom_plugins/jspolicy/                                    |
| javapolicy            | /workspaces/my-tool-migrater020226/kong-plugin-javapolicy/kong/plugins/javapolicy/             |
| kong-plugin-jspolicy  | /workspaces/my-tool-migrater020226/kong-plugin-jspolicy/kong/plugins/jspolicy/                 |
| pypolicy              | /workspaces/my-tool-migrater020226/kong-plugin-pypolicy/kong/plugins/pypolicy/                 |
| luafileexecuter       | /workspaces/my-tool-migrater020226/kong-custom-luafileexecuter/kong/plugins/luafileexecuter/   |

---

---


## Table of Contents
- [jspolicy](#jspolicy) — Lua Path: `custom_plugins/jspolicy/`
- [javascriptplugin](#javascriptplugin) — Lua Path: `custom_plugins/javascriptplugin/` (embedded in config)
- [javapolicy](#javapolicy) — Lua Path: `kong-plugin-javapolicy/kong/plugins/javapolicy/`
- [kong-plugin-jspolicy](#kong-plugin-jspolicy) — Lua Path: `kong-plugin-jspolicy/kong/plugins/jspolicy/`
- [luascriptfiles](#luascriptfiles) — Lua Path: `kong-plugin-luascriptfiles/kong/plugins/luascriptfiles/`
- [pypolicy](#pypolicy) — Lua Path: `kong-plugin-pypolicy/kong/plugins/pypolicy/`
- [luafileexecuter](#luafileexecuter) — Lua Path: `kong-custom-luafileexecuter/kong/plugins/luafileexecuter/`

---

## jspolicy

**Path:** `custom_plugins/jspolicy`  
**Lua Script Path:** `custom_plugins/jspolicy/` (scripts must be in the same directory as the plugin files)

**Description:**
Executes a main Lua script and an optional dependency script in request/response flow, with support for conditions, ordering, tagging, and key-value pairs.


**YAML Configuration Example:**
```yaml
plugins:
- name: jspolicy
  config:
    script_name: "main_policy.lua"      # Place this file in custom_plugins/jspolicy/
    dependency_name: "helper.lua"       # Place this file in custom_plugins/jspolicy/
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

**Parameters:**
| Name            | Required | Type    | Description                                      | Immutable |
|-----------------|----------|---------|--------------------------------------------------|-----------|
| script_name     | Yes      | string  | Main Lua script file name (must be in Lua Script Path) | No        |
| dependency_name | No       | string  | Dependency Lua script file name (must be in Lua Script Path) | No        |
| condition       | No       | string  | Lua condition for execution                      | No        |
| flow            | No       | string  | request/response/both (default: both)            | No        |
| kv_pairs        | No       | map     | Key-value pairs for script                       | No        |
| tags            | No       | array   | Kong plugin tags                                 | No        |
| ordering        | No       | object  | Plugin execution ordering                        | No        |

**Jinja Template:**
```jinja
plugins:
- name: jspolicy
  config:
    script_name: "{{ script_name }}"
    dependency_name: "{{ dependency_name }}"
    condition: "{{ condition }}"
    flow: "{{ flow }}"
    kv_pairs:
{% for k, v in kv_pairs.items() %}      {{ k }}: {{ v }}
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}
```

---

## javascriptplugin

**Path:** `custom_plugins/javascriptplugin`  
**Lua Script Path:** `custom_plugins/javascriptplugin/` (all scripts are embedded in config, not separate files)

**Description:**
Allows up to 10 Lua script blocks, each with an optional condition and phase (access, header_filter, body_filter, or both).

**YAML Configuration Example:**
```yaml
plugins:
- name: javascriptplugin
  config:
    script_1: |
      kong.log("Script 1 executed!")
    condition_1: "kong.request.get_method() == 'GET'"
    phase_1: "access"
    script_2: |
      kong.log("Script 2 executed!")
    phase_2: "header_filter"
    # ... up to script_10/condition_10/phase_10
  tags:
    - custom
    - javascript
  ordering:
    before:
      - rate-limiting
```

**Parameters:**
| Name         | Required | Type    | Description                                 | Immutable |
|--------------|----------|---------|---------------------------------------------|-----------|
| script_N     | Yes      | string  | Lua script block (N=1..10)                  | No        |
| condition_N  | No       | string  | Lua condition for script N                  | No        |
| phase_N      | No       | string  | access/header_filter/body_filter/both       | No        |
| tags         | No       | array   | Kong plugin tags                            | No        |
| ordering     | No       | object  | Plugin execution ordering                   | No        |

**Jinja Template:**
```jinja
plugins:
- name: javascriptplugin
  config:
{% for i in range(1, 11) %}    script_{{ i }}: "{{ scripts[i-1] }}"
    condition_{{ i }}: "{{ conditions[i-1] }}"
    phase_{{ i }}: "{{ phases[i-1] }}"
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}
```

---

## javapolicy

**Path:** `kong-plugin-javapolicy`  
**Lua Script Path:** `kong-plugin-javapolicy/kong/plugins/javapolicy/` (scripts must be in this directory)

**Description:**
Runs JavaScript-like policy logic in Lua, with support for main/dependency scripts, conditions, flow, and key-value pairs.

**YAML Configuration Example:**
```yaml
plugins:
- name: javapolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"
    condition: "ngx.var.request_method == 'GET'"
    flow: request
    kv_pairs:
      user_role: admin
      max_limit: "100"
  tags:
    - custom
    - policy
```

**Parameters:**
| Name            | Required | Type    | Description                                      | Immutable |
|-----------------|----------|---------|--------------------------------------------------|-----------|
| script_name     | Yes      | string  | Main Lua script file name                        | No        |
| dependency_name | No       | string  | Dependency Lua script file name                  | No        |
| condition       | No       | string  | Lua condition for execution                      | No        |
| flow            | No       | string  | request/response/both (default: both)            | No        |
| kv_pairs        | No       | map     | Key-value pairs for script                       | No        |
| tags            | No       | array   | Kong plugin tags                                 | No        |

**Jinja Template:**
```jinja
plugins:
- name: javapolicy
  config:
    script_name: "{{ script_name }}"
    dependency_name: "{{ dependency_name }}"
    condition: "{{ condition }}"
    flow: "{{ flow }}"
    kv_pairs:
{% for k, v in kv_pairs.items() %}      {{ k }}: {{ v }}
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}
```

---

## kong-plugin-jspolicy

**Path:** `kong-plugin-jspolicy`  
**Lua Script Path:** `kong-plugin-jspolicy/kong/plugins/jspolicy/` (scripts must be in this directory)

**Description:**
Same as jspolicy, but as a Kong plugin package. See jspolicy above for details.

**YAML Configuration Example:**
```yaml
plugins:
- name: jspolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"
    condition: "ngx.var.request_method == 'GET'"
    flow: request
    kv_pairs:
      user_role: admin
      max_limit: "100"
  tags:
    - custom
    - policy
```

**Jinja Template:**
```jinja
plugins:
- name: jspolicy
  config:
    script_name: "{{ script_name }}"
    dependency_name: "{{ dependency_name }}"
    condition: "{{ condition }}"
    flow: "{{ flow }}"
    kv_pairs:
{% for k, v in kv_pairs.items() %}      {{ k }}: {{ v }}
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}
```

---

## luascriptfiles

**Path:** `kong-plugin-luascriptfiles`  
**Lua Script Path:** `kong-plugin-luascriptfiles/kong/plugins/luascriptfiles/` (all script files must be in this directory)

**Description:**
Allows up to 20 Lua script files, each with an optional condition and flow (request/response/both).

**YAML Configuration Example:**
```yaml
plugins:
- name: luascriptfiles
  config:
    script1_name: "test_script1.lua"
    script1_condition: "kong.request.get_method() == 'GET'"
    script1_flow: "request"
    # ... up to script20_name/script20_condition/script20_flow
  tags:
    - custom
    - luascript
```

**Parameters:**
| Name              | Required | Type    | Description                                 | Immutable |
|-------------------|----------|---------|---------------------------------------------|-----------|
| scriptN_name      | Yes      | string  | Lua script file name (N=1..20)              | No        |
| scriptN_condition | No       | string  | Lua condition for script N                  | No        |
| scriptN_flow      | No       | string  | request/response/both (default: request)    | No        |
| tags              | No       | array   | Kong plugin tags                            | No        |

**Jinja Template:**
```jinja
plugins:
- name: luascriptfiles
  config:
{% for i in range(1, 21) %}    script{{ i }}_name: "{{ scripts[i-1] }}"
    script{{ i }}_condition: "{{ conditions[i-1] }}"
    script{{ i }}_flow: "{{ flows[i-1] }}"
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}
```

---

## pypolicy

**Path:** `kong-plugin-pypolicy`  
**Lua Script Path:** `kong-plugin-pypolicy/kong/plugins/pypolicy/` (scripts must be in this directory)

**Description:**
Template for creating Kong plugins similar to jspolicy. Supports main/dependency scripts, conditions, flow, and key-value pairs.

**YAML Configuration Example:**
```yaml
plugins:
- name: pypolicy
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"
    condition: "ngx.var.request_method == 'GET'"
    flow: request
    kv_pairs:
      user_role: admin
      max_limit: "100"
  tags:
    - custom
    - policy
```

**Jinja Template:**
```jinja
plugins:
- name: pypolicy
  config:
    script_name: "{{ script_name }}"
    dependency_name: "{{ dependency_name }}"
    condition: "{{ condition }}"
    flow: "{{ flow }}"
    kv_pairs:
{% for k, v in kv_pairs.items() %}      {{ k }}: {{ v }}
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}
```

---

## luafileexecuter

**Path:** `kong-custom-luafileexecuter`  
**Lua Script Path:** `kong-custom-luafileexecuter/kong/plugins/luafileexecuter/` (scripts must be in this directory)

**Description:**
Executes a Lua file with optional dependency, key-value pairs, tags, ordering, flow, and condition.

**YAML Configuration Example:**
```yaml
plugins:
- name: luafileexecuter
  config:
    script_name: "main_policy.lua"
    dependency_name: "helper.lua"
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

**Jinja Template:**
```jinja
plugins:
- name: luafileexecuter
  config:
    script_name: "{{ script_name }}"
    dependency_name: "{{ dependency_name }}"
    kv_pairs:
{% for k, v in kv_pairs.items() %}      {{ k }}: {{ v }}
{% endfor %}  tags:
{% for tag in tags %}    - {{ tag }}
{% endfor %}  ordering:
    before:
{% for b in ordering.before %}      - {{ b }}
{% endfor %}    after:
{% for a in ordering.after %}      - {{ a }}
{% endfor %}  flow: "{{ flow }}"
  condition: "{{ condition }}"
```

---
