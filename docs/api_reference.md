# API Reference

## Classes

### Templite

The main template engine class.

#### Constructor

```python
Templite(text, *contexts)
```

**Parameters:**
- `text` (str): The template text to compile
- `*contexts` (dict): Optional dictionaries of values available during rendering

**Example:**
```python
template = Templite("Hello {{name}}!", {'upper': str.upper})
```

#### Methods

##### render(context=None)

Render the template with the given context.

**Parameters:**
- `context` (dict, optional): Dictionary of values to use for rendering

**Returns:**
- `str`: The rendered template output

**Raises:**
- `KeyError`: If a required variable is missing from the context

**Example:**
```python
result = template.render({'name': 'World'})
```

### CodeBuilder

Helper class for generating Python code with proper indentation.

#### Constructor

```python
CodeBuilder(indent=0)
```

**Parameters:**
- `indent` (int): Initial indentation level

#### Methods

##### add_line(line)

Add a line of code with proper indentation.

**Parameters:**
- `line` (str): Line of code to add (without indentation or newline)

##### indent()

Increase indentation level for subsequent lines.

##### dedent()

Decrease indentation level for subsequent lines.

##### add_section()

Create a subsection that can be filled in later.

**Returns:**
- `CodeBuilder`: A new CodeBuilder instance for the section

##### get_globals()

Execute the generated code and return defined globals.

**Returns:**
- `dict`: Dictionary of global variables defined by the code

**Raises:**
- `AssertionError`: If indentation is not properly balanced

## Exceptions

### TempliteSyntaxError

Raised when there is a syntax error in the template.

**Inherits from:** `ValueError`

**Common causes:**
- Unmatched tags (missing `{% endif %}` or `{% endfor %}`)
- Invalid tag syntax
- Invalid variable names
- Unknown tags

## Template Syntax

### Variables

Variables are enclosed in `{{` and `}}`:

```html
{{variable}}
{{object.attribute}}
{{dict.key}}
{{object.method}}
```

### Filters

Filters transform variables using the pipe operator `|`:

```html
{{variable|filter}}
{{text|upper|truncate}}
```

### Control Flow

#### If Statements

```html
{% if condition %}
    content when true
{% endif %}
```

#### For Loops

```html
{% for item in items %}
    {{item}}
{% endfor %}
```

### Comments

```html
{# This is a comment #}
{# 
   Multi-line
   comment 
#}
```

## Built-in Features

### Dot Notation Resolution

When encountering `obj.attr`, the engine tries in order:

1. `getattr(obj, 'attr')` - Attribute access
2. `obj['attr']` - Dictionary/mapping access
3. If the result is callable, call it automatically

### Automatic String Conversion

All variable outputs are automatically converted to strings using `str()`.

### Context Merging

Contexts are merged in this order (later values override earlier ones):

1. Constructor contexts (in order provided)
2. Render context

## Performance Characteristics

### Compilation

- One-time cost when creating Templite instance
- Parses template and generates optimized Python code
- Cost: O(template_size)

### Rendering

- Fast execution of pre-compiled Python function
- Cost: O(output_size + data_complexity)

### Memory

- Compiled templates store generated Python function
- Memory usage: O(template_complexity)

## Error Messages

### Syntax Errors

| Error | Cause | Example |
|-------|-------|---------|
| "Don't understand if" | Malformed if statement | `{% if %}` |
| "Don't understand for" | Malformed for statement | `{% for item %}` |
| "Don't understand tag" | Unknown tag | `{% unknown %}` |
| "Too many ends" | Unmatched end tag | `{% endif %}` without matching `{% if %}` |
| "Mismatched end tag" | Wrong end tag | `{% if %}...{% endfor %}` |
| "Unmatched action tag" | Missing end tag | `{% if %}` without `{% endif %}` |
| "Not a valid name" | Invalid variable name | `{{123invalid}}` |

### Runtime Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `KeyError` | Missing variable in context | Add variable to render context |
| `KeyError` | Missing attribute/key in dot notation | Ensure object has the attribute or key |
| `AttributeError` | Object doesn't support attribute access | Check object type |

## Best Practices

### Template Design

- Keep templates simple and readable
- Use filters for complex transformations
- Minimize logic in templates
- Use descriptive variable names

### Performance

- Compile templates once, render many times
- Keep context dictionaries small
- Use appropriate data structures for template data
- Pre-process data when possible

### Error Handling

- Always handle `TempliteSyntaxError` when compiling templates
- Provide default values for optional context variables
- Validate template data before rendering

### Security

- Never render templates from untrusted sources
- Sanitize user input before including in templates
- Be careful with callable objects in context
