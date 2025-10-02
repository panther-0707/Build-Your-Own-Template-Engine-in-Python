"""Advanced examples showing the power of the Templite template engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from templite import Templite
import json


def example_blog_post():
    """Generate a blog post with comments."""
    print("=== Blog Post Example ===")
    
    template_text = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{post.title}} - My Blog</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .meta { color: #666; font-size: 0.9em; }
            .content { line-height: 1.6; margin: 20px 0; }
            .tags { margin: 10px 0; }
            .tag { background: #e0e0e0; padding: 2px 6px; border-radius: 3px; margin-right: 5px; }
            .comments { border-top: 1px solid #ddd; padding-top: 20px; margin-top: 30px; }
            .comment { margin: 15px 0; padding: 10px; background: #f9f9f9; }
            .comment-author { font-weight: bold; }
        </style>
    </head>
    <body>
        <article>
            <h1>{{post.title}}</h1>
            
            <div class="meta">
                By {{post.author}} on {{post.date}} 
                {% if post.tags %}
                    <div class="tags">
                        Tags: 
                        {% for tag in post.tags %}
                            <span class="tag">{{tag}}</span>
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            
            <div class="content">
                {{post.content|markdown}}
            </div>
        </article>
        
        {% if comments %}
            <div class="comments">
                <h3>Comments ({{comments|length}})</h3>
                {% for comment in comments %}
                    <div class="comment">
                        <div class="comment-author">{{comment.author}}</div>
                        <div class="comment-date">{{comment.date}}</div>
                        <div class="comment-content">{{comment.content}}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </body>
    </html>
    """
    
    # Simple markdown-like filter
    def markdown(text):
        lines = text.split('\n')
        result = []
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                result.append(f'<h2>{line[2:]}</h2>')
            elif line.startswith('## '):
                result.append(f'<h3>{line[3:]}</h3>')
            elif line:
                result.append(f'<p>{line}</p>')
        return '\n'.join(result)
    
    def length(items):
        return len(items)
    
    class Post:
        def __init__(self, title, author, date, content, tags=None):
            self.title = title
            self.author = author
            self.date = date
            self.content = content
            self.tags = tags or []
    
    class Comment:
        def __init__(self, author, date, content):
            self.author = author
            self.date = date
            self.content = content
    
    template = Templite(template_text, {
        'markdown': markdown,
        'length': length
    })
    
    post = Post(
        "Getting Started with Template Engines",
        "Jane Developer",
        "2023-10-15",
        """# Introduction
        
        Template engines are powerful tools for generating dynamic content.
        
        ## Why Use Templates?
        
        Templates separate logic from presentation, making code more maintainable.
        
        They're especially useful for web applications and report generation.""",
        ["programming", "templates", "web-development"]
    )
    
    comments = [
        Comment("Alice", "2023-10-16", "Great article! Very helpful."),
        Comment("Bob", "2023-10-17", "I've been looking for something like this."),
        Comment("Carol", "2023-10-18", "The examples are really clear.")
    ]
    
    result = template.render({
        'post': post,
        'comments': comments
    })
    
    print("Generated blog post HTML (first 500 chars):")
    print(result[:500] + "...")
    print()


def example_data_report():
    """Generate a data report with tables and charts."""
    print("=== Data Report Example ===")
    
    template_text = """
    <html>
    <head>
        <title>{{report_title}}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .summary { background: #e7f3ff; padding: 15px; margin: 20px 0; }
            .metric { display: inline-block; margin: 10px 20px; }
            .metric-value { font-size: 2em; font-weight: bold; color: #2c5aa0; }
            .metric-label { font-size: 0.9em; color: #666; }
        </style>
    </head>
    <body>
        <h1>{{report_title}}</h1>
        <p>Generated on {{generation_date}}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="metric">
                <div class="metric-value">{{total_sales|currency}}</div>
                <div class="metric-label">Total Sales</div>
            </div>
            <div class="metric">
                <div class="metric-value">{{total_orders}}</div>
                <div class="metric-label">Total Orders</div>
            </div>
            <div class="metric">
                <div class="metric-value">{{avg_order_value|currency}}</div>
                <div class="metric-label">Avg Order Value</div>
            </div>
        </div>
        
        <h2>Sales by Product</h2>
        <table>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Quantity Sold</th>
                    <th>Revenue</th>
                    <th>% of Total</th>
                </tr>
            </thead>
            <tbody>
                {% for product in products %}
                    <tr>
                        <td>{{product.name}}</td>
                        <td>{{product.quantity}}</td>
                        <td>{{product.revenue|currency}}</td>
                        <td>{{product.percentage|percent}}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
        
        {% if regions %}
            <h2>Sales by Region</h2>
            <table>
                <thead>
                    <tr>
                        <th>Region</th>
                        <th>Sales</th>
                        <th>Growth</th>
                    </tr>
                </thead>
                <tbody>
                    {% for region in regions %}
                        <tr>
                            <td>{{region.name}}</td>
                            <td>{{region.sales|currency}}</td>
                            <td>{{region.growth|percent}}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endif %}
    </body>
    </html>
    """
    
    def currency(amount):
        return f"${amount:,.2f}"
    
    def percent(value):
        return f"{value:.1f}%"
    
    class Product:
        def __init__(self, name, quantity, revenue, percentage):
            self.name = name
            self.quantity = quantity
            self.revenue = revenue
            self.percentage = percentage
    
    class Region:
        def __init__(self, name, sales, growth):
            self.name = name
            self.sales = sales
            self.growth = growth
    
    template = Templite(template_text, {
        'currency': currency,
        'percent': percent
    })
    
    products = [
        Product("Widget A", 150, 15000, 35.2),
        Product("Widget B", 120, 18000, 42.3),
        Product("Widget C", 80, 9600, 22.5)
    ]
    
    regions = [
        Region("North America", 25000, 12.5),
        Region("Europe", 18600, 8.3),
        Region("Asia Pacific", 14200, 15.7)
    ]
    
    context = {
        'report_title': 'Q3 2023 Sales Report',
        'generation_date': '2023-10-15',
        'total_sales': 42600,
        'total_orders': 350,
        'avg_order_value': 121.71,
        'products': products,
        'regions': regions
    }
    
    result = template.render(context)
    
    # Save report
    output_file = os.path.join(os.path.dirname(__file__), 'sales_report.html')
    with open(output_file, 'w') as f:
        f.write(result)
    
    print(f"Generated sales report saved as '{output_file}'")
    print()


def example_email_template():
    """Generate personalized email templates."""
    print("=== Email Template Example ===")
    
    template_text = """
    Subject: {{subject}}
    
    Dear {{recipient.name|title}},
    
    {% if is_welcome %}
        Welcome to {{company_name}}! We're excited to have you as a customer.
        
        Your account has been created successfully. Here are your account details:
        - Username: {{recipient.username}}
        - Email: {{recipient.email}}
        
        {% if welcome_bonus %}
            As a welcome bonus, you've received {{welcome_bonus|currency}} in store credit!
        {% endif %}
        
    {% endif %}
    
    {% if is_order_confirmation %}
        Thank you for your order! Here are the details:
        
        Order #: {{order.number}}
        Order Date: {{order.date}}
        
        Items:
        {% for item in order.items %}
        - {{item.name}} x {{item.quantity}} = {{item.total|currency}}
        {% endfor %}
        
        Total: {{order.total|currency}}
        
    {% endif %}
    
    {% if is_newsletter %}
        Here's what's new at {{company_name}}:
        
        {% for article in articles %}
        • {{article.title}}
          {{article.summary}}
          Read more: {{article.url}}
        
        {% endfor %}
        
    {% endif %}
    
    {% if footer_links %}
        ---
        {% for link in footer_links %}
        {{link.text}}: {{link.url}}
        {% endfor %}
    {% endif %}
    
    Best regards,
    The {{company_name}} Team
    """
    
    def currency(amount):
        return f"${amount:.2f}"
    
    class Recipient:
        def __init__(self, name, email, username=None):
            self.name = name
            self.email = email
            self.username = username
    
    class Order:
        def __init__(self, number, date, items, total):
            self.number = number
            self.date = date
            self.items = items
            self.total = total
    
    class OrderItem:
        def __init__(self, name, quantity, total):
            self.name = name
            self.quantity = quantity
            self.total = total
    
    class Article:
        def __init__(self, title, summary, url):
            self.title = title
            self.summary = summary
            self.url = url
    
    class Link:
        def __init__(self, text, url):
            self.text = text
            self.url = url
    
    template = Templite(template_text, {
        'currency': currency,
        'title': str.title
    })
    
    # Welcome email
    recipient1 = Recipient("john smith", "john@example.com", "johnsmith123")
    welcome_context = {
        'subject': 'Welcome to TechStore!',
        'is_welcome': True,
        'is_order_confirmation': False,
        'is_newsletter': False,
        'recipient': recipient1,
        'company_name': 'TechStore',
        'welcome_bonus': 10.00,
        'order': None,
        'articles': [],
        'footer_links': [
            Link('Unsubscribe', 'https://example.com/unsubscribe'),
            Link('Contact Us', 'https://example.com/contact')
        ]
    }
    
    welcome_email = template.render(welcome_context)
    print("Welcome Email:")
    print(welcome_email)
    print("-" * 50)
    
    # Order confirmation email
    recipient2 = Recipient("alice johnson", "alice@example.com")
    order = Order("ORD-12345", "2023-10-15", [
        OrderItem("Laptop", 1, 999.99),
        OrderItem("Mouse", 2, 50.00)
    ], 1049.99)
    
    order_context = {
        'subject': 'Order Confirmation #ORD-12345',
        'is_welcome': False,
        'is_order_confirmation': True,
        'is_newsletter': False,
        'recipient': recipient2,
        'company_name': 'TechStore',
        'order': order,
        'welcome_bonus': None,
        'articles': [],
        'footer_links': [
            Link('Track Your Order', 'https://example.com/track/ORD-12345'),
            Link('Contact Us', 'https://example.com/contact')
        ]
    }
    
    order_email = template.render(order_context)
    print("Order Confirmation Email:")
    print(order_email)
    print("-" * 50)


def example_code_generator():
    """Use templates to generate code."""
    print("=== Code Generator Example ===")
    
    class_template = """
    class {{class_name}}:
        \"\"\"{{class_description}}\"\"\"
        
        def __init__(self{% for field in fields %}, {{field.name}}{% endfor %}):
            \"\"\"Initialize {{class_name}}.\"\"\"
            {% for field in fields %}
            self.{{field.name}} = {{field.name}}
            {% endfor %}
        
        {% for field in fields %}
        {% if field.type == 'str' %}
        def get_{{field.name}}(self):
            \"\"\"Get {{field.name}}.\"\"\"
            return self.{{field.name}}
        
        def set_{{field.name}}(self, value):
            \"\"\"Set {{field.name}}.\"\"\"
            if not isinstance(value, str):
                raise TypeError("{{field.name}} must be a string")
            self.{{field.name}} = value
        
        {% endif %}
        {% endfor %}
        def __str__(self):
            return f"{{class_name}}({% for field in fields %}{{field.name}}={{self.{{field.name}}!r}}{% if not loop.last %}, {% endif %}{% endfor %})"
        
        def __repr__(self):
            return self.__str__()
    """
    
    # Note: This is a simplified version since we don't have loop.last
    simple_class_template = """
class {{class_name}}:
    \"\"\"{{class_description}}\"\"\"
    
    def __init__(self{% for field in fields %}, {{field.name}}{% endfor %}):
        \"\"\"Initialize {{class_name}}.\"\"\"
        {% for field in fields %}
        self.{{field.name}} = {{field.name}}
        {% endfor %}
    
    def __str__(self):
        fields = [{% for field in fields %}"{{field.name}}={self.{{field.name}}!r}"{% endfor %}]
        return f"{{class_name}}({', '.join(fields)})"
    
    def to_dict(self):
        \"\"\"Convert to dictionary.\"\"\"
        return {
            {% for field in fields %}
            "{{field.name}}": self.{{field.name}},
            {% endfor %}
        }
    """
    
    class Field:
        def __init__(self, name, type_name):
            self.name = name
            self.type = type_name
    
    template = Templite(simple_class_template)
    
    # Generate a Person class
    person_context = {
        'class_name': 'Person',
        'class_description': 'Represents a person with basic information.',
        'fields': [
            Field('name', 'str'),
            Field('age', 'int'),
            Field('email', 'str')
        ]
    }
    
    person_code = template.render(person_context)
    
    print("Generated Person class:")
    print(person_code)
    
    # Save generated code
    with open(os.path.join(os.path.dirname(__file__), 'generated_person.py'), 'w') as f:
        f.write(person_code)
    
    print("Generated code saved as 'generated_person.py'")


if __name__ == '__main__':
    example_blog_post()
    example_data_report()
    example_email_template()
    example_code_generator()
    
    print("\n=== Advanced Examples Complete ===")
    print("These examples show how Templite can be used for various")
    print("text generation tasks beyond simple web pages.")
