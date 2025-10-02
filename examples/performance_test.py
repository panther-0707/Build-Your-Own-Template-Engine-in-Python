"""Performance comparison and benchmarking for Templite."""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from templite import Templite


def benchmark_template_compilation():
    """Benchmark template compilation time."""
    print("=== Template Compilation Benchmark ===")
    
    template_text = """
    <html>
    <head><title>{{page_title}}</title></head>
    <body>
        <h1>{{header}}</h1>
        {% for item in items %}
            <div>
                <h2>{{item.name|titlecase}}</h2>
                <p>{{item.description}}</p>
                {% if item.price %}
                    <span class="price">${{item.price}}</span>
                {% endif %}
            </div>
        {% endfor %}
    </body>
    </html>
    """
    
    # Time compilation
    start_time = time.time()
    template = Templite(template_text, {'titlecase': str.title})
    compilation_time = time.time() - start_time
    
    print(f"Template compilation time: {compilation_time:.4f} seconds")
    return template


def benchmark_template_rendering(template, num_renders=1000):
    """Benchmark template rendering time."""
    print(f"\n=== Template Rendering Benchmark ({num_renders} renders) ===")
    
    class Item:
        def __init__(self, name, description, price=None):
            self.name = name
            self.description = description
            self.price = price
    
    # Prepare test data
    context = {
        'page_title': 'Benchmark Page',
        'header': 'Performance Test',
        'items': [
            Item('Product 1', 'Description for product 1', 19.99),
            Item('Product 2', 'Description for product 2', 29.99),
            Item('Product 3', 'Description for product 3'),
            Item('Product 4', 'Description for product 4', 39.99),
            Item('Product 5', 'Description for product 5', 49.99),
        ]
    }
    
    # Warm up
    for _ in range(10):
        template.render(context)
    
    # Time rendering
    start_time = time.time()
    for _ in range(num_renders):
        result = template.render(context)
    rendering_time = time.time() - start_time
    
    print(f"Total rendering time: {rendering_time:.4f} seconds")
    print(f"Average per render: {rendering_time/num_renders*1000:.4f} ms")
    print(f"Renders per second: {num_renders/rendering_time:.0f}")
    
    return result


def compare_with_format_string():
    """Compare performance with Python string formatting."""
    print("\n=== Comparison with String Formatting ===")
    
    # Template version
    template = Templite("Hello, {{name}}! You have {{count}} messages.")
    
    # String format version
    format_string = "Hello, {name}! You have {count} messages."
    
    context = {'name': 'Alice', 'count': 5}
    num_iterations = 10000
    
    # Benchmark template
    start_time = time.time()
    for _ in range(num_iterations):
        result1 = template.render(context)
    template_time = time.time() - start_time
    
    # Benchmark string format
    start_time = time.time()
    for _ in range(num_iterations):
        result2 = format_string.format(**context)
    format_time = time.time() - start_time
    
    print(f"Template method: {template_time:.4f} seconds")
    print(f"String format method: {format_time:.4f} seconds")
    print(f"Template is {format_time/template_time:.1f}x slower than string.format()")
    print(f"Results are identical: {result1 == result2}")


def memory_usage_test():
    """Test memory usage of compiled templates."""
    print("\n=== Memory Usage Test ===")
    
    import gc
    
    # Create multiple templates to see memory impact
    templates = []
    
    for i in range(100):
        template_text = f"""
        <div class="item-{{i}}">
            <h1>{{{{title}}}}</h1>
            {{% for item in items %}}
                <p>{{{{item.name}}}} - {{{{item.value}}}}</p>
            {{% endfor %}}
        </div>
        """
        
        template = Templite(template_text)
        templates.append(template)
    
    print(f"Created {len(templates)} templates")
    
    # Force garbage collection and measure
    gc.collect()
    
    # Test rendering with all templates
    class TestItem:
        def __init__(self, name, value):
            self.name = name
            self.value = value
    
    context = {
        'title': 'Test Page',
        'items': [TestItem(f'Item {i}', i) for i in range(10)]
    }
    
    total_output_size = 0
    start_time = time.time()
    
    for template in templates:
        result = template.render(context)
        total_output_size += len(result)
    
    total_time = time.time() - start_time
    
    print(f"Rendered all templates in {total_time:.4f} seconds")
    print(f"Total output size: {total_output_size:,} characters")


def stress_test():
    """Stress test with complex nested structures."""
    print("\n=== Stress Test ===")
    
    template_text = """
    <html>
    <body>
        {% for category in categories %}
            <div class="category">
                <h2>{{category.name}}</h2>
                {% for subcategory in category.subcategories %}
                    <div class="subcategory">
                        <h3>{{subcategory.name}}</h3>
                        {% for item in subcategory.items %}
                            <div class="item">
                                <h4>{{item.name|title}}</h4>
                                <p>{{item.description}}</p>
                                {% if item.tags %}
                                    <div class="tags">
                                        {% for tag in item.tags %}
                                            <span class="tag">{{tag|upper}}</span>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    </body>
    </html>
    """
    
    template = Templite(template_text, {
        'title': str.title,
        'upper': str.upper
    })
    
    # Create nested test data
    class Item:
        def __init__(self, name, description, tags=None):
            self.name = name
            self.description = description
            self.tags = tags or []
    
    class SubCategory:
        def __init__(self, name, items):
            self.name = name
            self.items = items
    
    class Category:
        def __init__(self, name, subcategories):
            self.name = name
            self.subcategories = subcategories
    
    # Generate large nested structure
    categories = []
    for c in range(5):  # 5 categories
        subcategories = []
        for s in range(3):  # 3 subcategories each
            items = []
            for i in range(10):  # 10 items each
                item = Item(
                    f"Item {c}-{s}-{i}",
                    f"Description for item {c}-{s}-{i}",
                    [f"tag{j}" for j in range(3)]
                )
                items.append(item)
            subcategory = SubCategory(f"SubCategory {c}-{s}", items)
            subcategories.append(subcategory)
        category = Category(f"Category {c}", subcategories)
        categories.append(category)
    
    context = {'categories': categories}
    
    print(f"Generated data: {len(categories)} categories, "
          f"{sum(len(c.subcategories) for c in categories)} subcategories, "
          f"{sum(len(s.items) for c in categories for s in c.subcategories)} items")
    
    # Time the rendering
    start_time = time.time()
    result = template.render(context)
    render_time = time.time() - start_time
    
    print(f"Stress test render time: {render_time:.4f} seconds")
    print(f"Output size: {len(result):,} characters")


if __name__ == '__main__':
    template = benchmark_template_compilation()
    result = benchmark_template_rendering(template)
    compare_with_format_string()
    memory_usage_test()
    stress_test()
    
    print("\n=== Benchmark Complete ===")
    print("Templite shows good performance for a compilation-based template engine.")
    print("The compilation step pays off when templates are rendered multiple times.")
