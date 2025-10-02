# Architecture Overview

## Design Philosophy

Templite follows a **compilation-based** approach to template rendering, prioritizing performance for scenarios where templates are rendered multiple times. The design is inspired by Django's template syntax but implements a simpler, more focused feature set.

## Key Design Decisions

### Compilation vs Interpretation

**Chosen Approach: Compilation**

- Templates are compiled to Python functions once
- Rendering executes pre-compiled code
- Better performance for repeated rendering
- More complex implementation but faster execution

**Alternative: Interpretation**

- Parse template into data structure
- Walk data structure during rendering
- Simpler implementation but slower repeated rendering
- Used by Django's template engine

### Code Generation Strategy

The engine generates optimized Python code with several micro-optimizations:

1. **Local Variable Caching**: Context variables are extracted to locals
2. **Method Reference Caching**: `result.append` is cached as `append_result`
3. **Built-in Caching**: `str` is cached as `to_str`
4. **String Building**: Uses list + join instead of string concatenation

## Architecture Components

### 1. CodeBuilder (`codebuilder.py`)

**Purpose**: Manages Python code generation with proper indentation.

**Key Features**:
- Automatic indentation management
- Section support for deferred code insertion
- Code execution and global extraction

**Design Pattern**: Builder Pattern
- Incrementally constructs complex Python code
- Handles state (indentation level) automatically
- Provides fluent interface for code construction

```python
code = CodeBuilder()
code.add_line("def func():")
code.indent()
section = code.add_section()  # Fill this later
code.add_line("return result")
code.dedent()

# Later...
section.add_line("result = 42")
```

### 2. Exception Handling (`exceptions.py`)

**Purpose**: Provides clear error messages for template syntax issues.

**Design Pattern**: Exception Hierarchy
- Single exception type for all syntax errors
- Descriptive error messages with context

### 3. Template Engine (`templite.py`)

**Purpose**: Main template compilation and rendering logic.

**Key Components**:

#### Parser
- Regex-based tokenization
- Token classification (literal, expression, tag, comment)
- Recursive expression parsing

#### Compiler
- Converts tokens to Python code
- Manages variable tracking
- Handles control flow structures

#### Runtime
- Context management and merging
- Dot notation resolution
- Rendering coordination

## Compilation Process

### Phase 1: Tokenization

```python
tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
```

**Input**: Template string
**Output**: List of tokens (literals, expressions, tags, comments)

**Example**:
```
"Hello {{name}}!" → ["Hello ", "{{name}}", "!"]
```

### Phase 2: Code Generation

**Process**:
1. Initialize CodeBuilder with function header
2. Create variable extraction section
3. Process each token:
   - Literals → Add to output buffer
   - Expressions → Compile and add to buffer
   - Tags → Generate control flow code
   - Comments → Ignore
4. Fill variable extraction section
5. Add function return statement

**Generated Code Structure**:
```python
def render_function(context, do_dots):
    # Variable extraction section (filled later)
    c_var1 = context['var1']
    c_var2 = context['var2']
    
    # Optimized locals
    result = []
    append_result = result.append
    extend_result = result.extend
    to_str = str
    
    # Template logic
    extend_result(['Hello ', to_str(c_name), '!'])
    
    return ''.join(result)
```

### Phase 3: Expression Compilation

**Recursive Process**:
1. Check for pipes (filters) → Split and process recursively
2. Check for dots (attribute access) → Convert to `do_dots` call
3. Base case: Simple variable → Convert to local variable reference

**Examples**:
```
"name" → "c_name"
"user.name" → "do_dots(c_user, 'name')"
"text|upper" → "c_upper(c_text)"
"user.name|title" → "c_title(do_dots(c_user, 'name'))"
```

## Rendering Process

### Phase 1: Context Preparation

```python
render_context = dict(self.context)  # Copy constructor context
if context:
    render_context.update(context)   # Merge render context
```

### Phase 2: Function Execution

```python
return self._render_function(render_context, self._do_dots)
```

The compiled function:
1. Extracts variables from context to locals
2. Builds result as list of strings
3. Joins strings and returns final output

## Dot Notation Resolution

**Strategy**: Try Multiple Access Methods

```python
def _do_dots(self, value, *dots):
    for dot in dots:
        try:
            value = getattr(value, dot)    # Try attribute
        except AttributeError:
            value = value[dot]             # Try key access
        if callable(value):
            value = value()                # Auto-call methods
    return value
```

**Flexibility Benefits**:
- `obj.attr` works for both `obj.attr` and `obj['attr']`
- Automatic method calling: `obj.method` calls `obj.method()`
- Unified syntax regardless of data structure

## Memory Management

### Template Storage
- Compiled templates store only the render function
- Original template text is not retained
- Minimal memory footprint per template

### Rendering Memory
- Uses list building for string concatenation
- Temporary string list is garbage collected after rendering
- No persistent state between renders

## Performance Optimizations

### Compilation Time Optimizations
- Single regex pass for tokenization
- Minimal AST construction (direct code generation)
- Efficient variable tracking with sets

### Runtime Optimizations
- Pre-cached method references
- Local variable access (faster than globals/builtins)
- List building instead of string concatenation
- Batch string operations with `extend_result`

### Micro-optimizations
```python
# Instead of:
result.append("hello")
result.append("world")

# Generate:
extend_result(["hello", "world"])
```

## Error Handling Strategy

### Compilation Errors
- Immediate validation during parsing
- Clear error messages with context
- Fail-fast approach prevents runtime surprises

### Runtime Errors
- Minimal error handling overhead
- Natural Python exceptions (KeyError, AttributeError)
- Predictable error behavior

## Extensibility Points

### Limited by Design
Templite is intentionally minimal and not designed for extensive customization:

**What's Extensible**:
- Filter functions (passed in context)
- Data objects and their methods
- Context preparation logic

**What's Not Extensible**:
- Template syntax
- Control flow structures
- Built-in operations

### Why Limited Extensibility?

1. **Simplicity**: Easy to understand and maintain
2. **Performance**: Fewer abstraction layers
3. **Educational Purpose**: Clear, focused implementation
4. **Reliability**: Fewer moving parts, fewer bugs

## Comparison with Alternatives

### vs Django Templates
- **Similarity**: Syntax inspiration
- **Difference**: Compilation vs interpretation
- **Tradeoff**: Templite is faster but less flexible

### vs Jinja2
- **Similarity**: Compilation approach
- **Difference**: Feature scope
- **Tradeoff**: Templite is simpler but less powerful

### vs String Formatting
- **Similarity**: Variable substitution
- **Difference**: Control flow support
- **Tradeoff**: Templite supports logic but is slower for simple cases

## Future Considerations

**If extending Templite**:
1. Template inheritance would require significant architecture changes
2. Custom tags would need a plugin system
3. Automatic escaping would require output context tracking
4. More control flow would complicate the parser

**Better alternatives for production**:
- Django templates for Django applications
- Jinja2 for full-featured templating
- Built-in string formatting for simple cases
