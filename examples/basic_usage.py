"""Basic usage examples for the Templite template engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from templite import Templite


def example_basic():
    """Basic variable substitution."""
    print("=== Basic Example ===")
    template = Templite("Hello, {{name}}!")
    result = template.render({'name': 'World'})
    print(f"Template: Hello, {{{{name}}}}!")
    print(f"Result: {result}")
    print()


def example_with_filters():
    """Example using filters."""
    print("=== Filter Example ===")
    
    def upper(text):
        return text.upper()
    
    def add_exclamation(text):
        return text + "!!!"
    
    template = Templite(
        "{{greeting|upper|add_exclamation}}",
        {'upper': upper, 'add_exclamation': add_exclamation}
    )
    
    result = template.render({'greeting': 'hello world'})
    print("Template: {{greeting|upper|add_exclamation}}")
    print(f"Result: {result}")
    print()


def example_conditionals():
    """Example using conditionals."""
    print("=== Conditional Example ===")
    
    template_text = """
    {% if user_logged_in %}
        Welcome back, {{username}}!
    {% endif %}
    {% if show_login %}
        Please log in.
    {% endif %}
    """.strip()
    
    template = Templite(template_text)
    
    # User logged in
    result1 = template.render({
        'user_logged_in': True,
        'show_login': False,
        'username': 'Alice'
    })
    print("User logged in:")
    print(result1)
    print()
    
    # User not logged in
    result2 = template.render({
        'user_logged_in': False,
        'show_login': True,
        'username': 'Alice'
    })
    print("User not logged in:")
    print(result2)
    print()


def example_loops():
    """Example using loops."""
    print("=== Loop Example ===")
    
    template_text = """
    <h2>Shopping List:</h2>
    <ul>
    {% for item in items %}
        <li>{{item.name}} - ${{item.price}}</li>
    {% endfor %}
    </ul>
    """.strip()
    
    class Item:
        def __init__(self, name, price):
            self.name = name
            self.price = price
    
    template = Templite(template_text)
    
    items = [
        Item("Apple", "1.00"),
        Item("Banana", "0.50"),
        Item("Orange", "0.75")
    ]
    
    result = template.render({'items': items})
    print("Template with items:")
    print(result)
    print()


def example_complex():
    """Complex example combining all features."""
    print("=== Complex Example ===")
    
    template_text = """
    <html>
    <head>
        <title>{{page_title}}</title>
    </head>
    <body>
        <h1>Welcome to {{site_name}}!</h1>
        
        {% if user %}
            <p>Hello, {{user.name|title}}!</p>
            {% if user.is_premium %}
                <div class="premium-badge">Premium Member</div>
            {% endif %}
        {% endif %}
        
        <h2>Latest Products:</h2>
        {% for product in products %}
            <div class="product">
                <h3>{{product.name}}</h3>
                <p>Price: {{product.price|currency}}</p>
                <p>{{product.description|truncate}}</p>
            </div>
        {% endfor %}
        
        {# This is a comment and won't appear in the output #}
        <footer>
            <p>&copy; 2023 {{site_name}}</p>
        </footer>
    </body>
    </html>
    """.strip()
    
    # Define helper functions
    def currency(price):
        return f"${float(price):.2f}"
    
    def truncate(text, length=50):
        return text[:length] + "..." if len(text) > length else text
    
    # Define data classes
    class User:
        def __init__(self, name, is_premium=False):
            self.name = name
            self.is_premium = is_premium
    
    class Product:
        def __init__(self, name, price, description):
            self.name = name
            self.price = price
            self.description = description
    
    # Create template with helper functions
    template = Templite(template_text, {
        'title': str.title,
        'currency': currency,
        'truncate': truncate
    })
    
    # Prepare data
    user = User("john doe", True)
    products = [
        Product("Laptop", "999.99", "High-performance laptop for professionals with excellent battery life and fast processor"),
        Product("Mouse", "25.50", "Ergonomic wireless mouse"),
        Product("Keyboard", "75.00", "Mechanical keyboard with RGB lighting")
    ]
    
    context = {
        'page_title': 'Our Store',
        'site_name': 'TechShop',
        'user': user,
        'products': products
    }
    
    result = template.render(context)
    print("Complex template result:")
    print(result)
    print()


def example_web_page():
    """Example of generating a complete web page."""
    print("=== Web Page Example ===")
    
    template_text = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{title}}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background: #f0f0f0; padding: 10px; }
            .product { border: 1px solid #ccc; margin: 10px 0; padding: 10px; }
            .price { font-weight: bold; color: green; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{title}}</h1>
        </div>
        
        <p>Welcome, {{user_name}}!</p>
        
        <h2>Products:</h2>
        {% for product in product_list %}
            <div class="product">
                <h3>{{product.name}}</h3>
                <p class="price">{{product.price|format_price}}</p>
            </div>
        {% endfor %}
    </body>
    </html>
    """.strip()
    
    def format_price(price):
        return f"${price:.2f}"
    
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price
    
    template = Templite(template_text, {'format_price': format_price})
    
    context = {
        'title': 'Product Catalog',
        'user_name': 'Charlie',
        'product_list': [
            Product('Apple', 1.00),
            Product('Fig', 1.50),
            Product('Pomegranate', 3.25)
        ]
    }
    
    result = template.render(context)
    
    # Write to file
    with open(os.path.join(os.path.dirname(__file__), 'output.html'), 'w') as f:
        f.write(result)
    
    print("Generated web page saved as 'output.html'")
    print("First few lines of the result:")
    print('\n'.join(result.split('\n')[:15]) + '\n...')
    print()


if __name__ == '__main__':
    example_basic()
    example_with_filters() 
    example_conditionals()
    example_loops()
    example_complex()
    example_web_page()
