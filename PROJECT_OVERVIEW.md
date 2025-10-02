# Templite Template Engine

## Project Structure

```
Template-Engine/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── templite.py        # Main template engine
│   ├── codebuilder.py     # Code generation helper
│   └── exceptions.py      # Custom exceptions
├── tests/                 # Test suite
│   ├── test_templite.py   # Main engine tests
│   ├── test_codebuilder.py # CodeBuilder tests
│   └── run_tests.py       # Test runner
├── examples/              # Usage examples
│   ├── basic_usage.py     # Simple examples
│   ├── advanced_examples.py # Complex use cases
│   └── performance_test.py # Benchmarking
├── docs/                  # Documentation
│   ├── api_reference.md   # API documentation
│   └── architecture.md    # Design overview
├── README.md             # Main documentation
└── setup.py             # Installation script
```

## Quick Start

1. **Basic Usage**:
   ```python
   from src.templite import Templite
   template = Templite("Hello {{name}}!")
   print(template.render({'name': 'World'}))
   ```

2. **Run Tests**:
   ```bash
   cd tests
   python run_tests.py
   ```

3. **See Examples**:
   ```bash
   cd examples
   python basic_usage.py
   ```

## Features

✅ Variable substitution with `{{var}}`  
✅ Dot notation: `{{obj.attr}}`, `{{dict.key}}`  
✅ Filters with pipes: `{{text|upper|truncate}}`  
✅ Conditionals: `{% if condition %}...{% endif %}`  
✅ Loops: `{% for item in items %}...{% endfor %}`  
✅ Comments: `{# This won't appear #}`  
✅ Fast compilation to Python code  
✅ Comprehensive test coverage  

## Implementation Details

- **252 lines** of core template engine code
- **275 lines** of comprehensive tests
- **Compilation-based** approach for performance
- **Django-inspired** syntax
- **Educational implementation** from "500 Lines or Less"

## Files Overview

| File | Purpose | Lines |
|------|---------|-------|
| `templite.py` | Main template engine | 252 |
| `codebuilder.py` | Code generation | 45 |
| `exceptions.py` | Error handling | 5 |
| `test_templite.py` | Comprehensive tests | 275+ |
| `examples/*.py` | Usage demonstrations | 300+ |

Total implementation: **~500 lines** (excluding tests and examples)

## Usage Examples

### Web Page Generation
Generate complete HTML pages with dynamic content.

### Email Templates  
Create personalized email messages with conditionals.

### Report Generation
Build data reports with tables and formatting.

### Code Generation
Use templates to generate source code files.

## Performance

- Templates compile once, render many times
- Optimized Python code generation
- Local variable caching for speed
- Efficient string building with lists

## Architecture

1. **Tokenization**: Split template using regex
2. **Code Generation**: Build optimized Python function
3. **Compilation**: Execute generated code 
4. **Rendering**: Call compiled function with data

## Educational Value

This implementation demonstrates:
- Template engine design patterns
- Code generation techniques
- Parsing and compilation concepts
- Performance optimization strategies
- Comprehensive testing approaches

Perfect for understanding how template engines work under the hood!
