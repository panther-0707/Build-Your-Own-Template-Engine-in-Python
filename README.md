# Templite: Build Your Own Template Engine

A Python template engine project that teaches code generation and metaprogramming by building a working template compiler from scratch.

## Overview

Templite is a lightweight template engine that compiles templates into Python code for fast rendering. This project demonstrates how popular templating systems like Jinja2 and Django Templates work under the hood.

## Features

- **Variable Substitution**: `{{user_name}}`
- **Dot Notation**: `{{user.name}}` - Works with both attributes and dictionary keys
- **Filters**: `{{name|upper|escape}}` - Pipe values through transformation functions
- **Conditionals**: `{% if condition %}...{% endif %}`
- **Loops**: `{% for item in items %}...{% endfor %}`
- **Comments**: `{# This won't appear in output #}`

## Quick Start
```python
from templite import Templite

# Create a template
template = Templite('''
    <h1>Hello {{name|upper}}!</h1>
    {% for topic in topics %}
        <p>You are interested in {{topic}}.</p>
    {% endfor %}
    ''',
    {'upper': str.upper}
)

# Render with data
result = template.render({
    'name': 'Jules',
    'topics': ['Python', 'Templates', 'Code Generation']
})

print(result)