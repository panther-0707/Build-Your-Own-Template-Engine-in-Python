# Templite: A Simple Template Engine

A lightweight, fast template engine implementation in Python, based on the "500 Lines or Less" book chapter by Ned Batchelder.

## Features

- **Simple Syntax**: Django-inspired template syntax that's easy to learn and use
- **Fast Compilation**: Templates are compiled to Python code for optimal performance
- **Flexible Data Access**: Unified dot notation for attributes, dictionary keys, and method calls
- **Filter Support**: Apply functions to transform values in templates
- **Control Structures**: Support for conditionals (`if`) and loops (`for`)
- **Comments**: Template comments that don't appear in output
- **Lightweight**: Less than 300 lines of core code

## Quick Start

### Installation

Simply copy the `src` directory to your project or add it to your Python path.

```python
from templite import Templite

# Create a simple template
template = Templite("Hello, {{name}}!")

# Render with data
result = template.render({'name': 'World'})
print(result)  # Output: Hello, World!
```

### Basic Usage

```python
from templite import Templite

# Template with variables and filters
template = Templite('''
    <h1>Welcome, {{user.name|title}}!</h1>
    {% if user.is_premium %}
        <p>You are a premium member!</p>
    {% endif %}
    
    <h2>Your items:</h2>
    <ul>
    {% for item in items %}
        <li>{{item.name}} - {{item.price|currency}}</li>
    {% endfor %}
    </ul>
''', {
    'title': str.title,
    'currency': lambda x: f"${float(x):.2f}"
})

# Create data
class User:
    def __init__(self, name, is_premium):
        self.name = name
        self.is_premium = is_premium

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Render template
result = template.render({
    'user': User('alice smith', True),
    'items': [
        Item('Apple', 1.99),
        Item('Banana', 0.99)
    ]
})

print(result)
```

## Syntax Reference

### Variables

Variables are enclosed in double curly braces:

```html
{{variable_name}}
{{user.name}}
{{product.price}}
```

### Dot Notation

The template engine uses a unified dot notation that works for:
- Object attributes: `user.name`
- Dictionary keys: `data.key` (equivalent to `data['key']`)
- Method calls: `text.upper` (automatically calls `text.upper()`)

### Filters

Filters transform variable values using the pipe operator:

```html
{{name|upper}}
{{price|currency}}
{{text|escape|truncate}}
```

Filters are functions passed in the template context:

```python
template = Templite("{{text|upper}}", {'upper': str.upper})
```

### Conditionals

```html
{% if condition %}
    <p>This appears when condition is true</p>
{% endif %}

{% if user.is_authenticated %}
    <p>Welcome, {{user.name}}!</p>
{% endif %}
```

### Loops

```html
{% for item in items %}
    <li>{{item}}</li>
{% endfor %}

{% for product in products %}
    <div>{{product.name}}: {{product.price}}</div>
{% endfor %}
```

### Comments

Comments are ignored in the output:

```html
{# This is a comment and won't appear in the output #}
<p>This will appear</p>
{# 
   Multi-line comments
   are also supported
#}
```

## Advanced Features

### Constructor Context

You can provide global context when creating the template:

```python
template = Templite(
    "{{text|format_price}}", 
    {'format_price': lambda x: f"${x:.2f}"}
)

# The format_price filter is available in all renders
result = template.render({'text': 19.99})
```

### Nested Structures

Templates support arbitrary nesting of conditionals and loops:

```html
{% for category in categories %}
    <h2>{{category.name}}</h2>
    {% for item in category.items %}
        {% if item.available %}
            <p>{{item.name}} - In Stock</p>
        {% endif %}
    {% endfor %}
{% endfor %}
```

### Method Calls

Objects methods are automatically called when accessed:

```python
class Product:
    def __init__(self, name):
        self.name = name
    
    def get_description(self):
        return f"Description for {self.name}"

template = Templite("{{product.get_description}}")
result = template.render({'product': Product('Widget')})
# Output: Description for Widget
```

## Performance

Templite uses a compilation approach for optimal performance:

1. **Compilation Phase**: Templates are parsed and compiled to Python functions (done once)
2. **Rendering Phase**: The compiled function executes to generate output (done many times)

This makes Templite particularly efficient when the same template is rendered multiple times.

### Performance Tips

- Compile templates once and reuse them
- Use filters for expensive operations rather than complex template logic
- Keep template context as small as practical

## Error Handling

Templite provides clear error messages for common issues:

```python
from templite import TempliteSyntaxError

try:
    template = Templite("{% if condition %}")  # Missing endif
except TempliteSyntaxError as e:
    print(f"Template error: {e}")
```

Common errors:
- Unmatched tags (`{% if %}` without `{% endif %}`)
- Invalid variable names
- Wrong tag syntax
- Missing variables in context (raises `KeyError`)

## Examples

See the `examples/` directory for comprehensive examples:

- `basic_usage.py` - Simple template examples
- `advanced_examples.py` - Complex real-world use cases
- `performance_test.py` - Performance benchmarking

### Web Page Generation

```python
template = Templite('''
<!DOCTYPE html>
<html>
<head><title>{{title}}</title></head>
<body>
    <h1>{{header}}</h1>
    {% for section in sections %}
        <div class="section">
            <h2>{{section.title}}</h2>
            <p>{{section.content}}</p>
        </div>
    {% endfor %}
</body>
</html>
''')

result = template.render({
    'title': 'My Website',
    'header': 'Welcome!',
    'sections': [
        {'title': 'About', 'content': 'This is the about section.'},
        {'title': 'Contact', 'content': 'Contact us at info@example.com'}
    ]
})
```

### Email Templates

```python
email_template = Templite('''
Subject: Welcome to {{site_name}}!

Dear {{user.name}},

Thank you for joining {{site_name}}! 

{% if welcome_bonus %}
You've received a {{welcome_bonus|currency}} welcome bonus!
{% endif %}

Best regards,
The {{site_name}} Team
''', {
    'currency': lambda x: f"${x:.2f}"
})

result = email_template.render({
    'site_name': 'MyApp',
    'user': {'name': 'Alice'},
    'welcome_bonus': 10.0
})
```

## Testing

Run the comprehensive test suite:

```bash
cd tests
python run_tests.py
```

The test suite includes:
- Basic functionality tests
- Error handling tests
- Complex template scenarios
- Performance benchmarks

## Limitations

Templite is designed to be simple and lightweight. Features not included:

- Template inheritance (`extends`, `block`)
- Custom tags
- Automatic HTML escaping
- Complex conditional logic (`else`, `elif`)
- Multiple loop variables
- Whitespace control
- Filter arguments

For applications needing these features, consider using Django templates or Jinja2.

## Architecture

### CodeBuilder

The `CodeBuilder` class handles Python code generation with proper indentation:

```python
from codebuilder import CodeBuilder

code = CodeBuilder()
code.add_line("def func():")
code.indent()
code.add_line("return 42")
code.dedent()

print(str(code))  # Properly indented Python code
```

### Compilation Process

1. **Lexical Analysis**: Split template into tokens using regex
2. **Parsing**: Process tokens and generate Python code
3. **Code Generation**: Use CodeBuilder to create executable function
4. **Compilation**: Execute generated code to create render function

### Rendering Process

1. **Context Preparation**: Merge constructor and render contexts
2. **Function Execution**: Call compiled render function
3. **Output Generation**: Assemble result from string fragments

## Contributing

This implementation is based on the educational chapter from "500 Lines or Less". 
It's designed to be studied and understood rather than extended for production use.

For production applications, consider:
- Django templates for Django applications
- Jinja2 for standalone applications
- Mako for high-performance needs

## License

Based on the "500 Lines or Less" book chapter by Ned Batchelder.
Educational implementation - see original work for licensing details.

## References

- [500 Lines or Less: A Template Engine](http://aosabook.org/en/500L/a-template-engine.html)
- [Django Template Language](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/): Build Your Own Template Engine

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