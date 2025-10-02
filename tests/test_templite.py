"""Comprehensive test suite for the Templite template engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from templite import Templite, TempliteSyntaxError


class TestTemplite(unittest.TestCase):
    """Test the Templite template engine."""

    def test_empty_template(self):
        """Test an empty template."""
        t = Templite("")
        self.assertEqual(t.render(), "")

    def test_literal_text(self):
        """Test a template with only literal text."""
        t = Templite("Hello, World!")
        self.assertEqual(t.render(), "Hello, World!")

    def test_simple_variable(self):
        """Test a simple variable substitution."""
        t = Templite("Hello, {{name}}!")
        self.assertEqual(t.render({'name': 'World'}), "Hello, World!")

    def test_variable_not_in_context(self):
        """Test that missing variables raise an error."""
        t = Templite("Hello, {{name}}!")
        with self.assertRaises(KeyError):
            t.render({})

    def test_numbers(self):
        """Test numeric values."""
        t = Templite("{{num}}")
        self.assertEqual(t.render({'num': 42}), "42")
        self.assertEqual(t.render({'num': 3.14}), "3.14")

    def test_none_value(self):
        """Test None values."""
        t = Templite("{{val}}")
        self.assertEqual(t.render({'val': None}), "None")

    def test_attribute_access(self):
        """Test attribute access with dots."""
        class Obj:
            def __init__(self):
                self.attr = "value"

        t = Templite("{{obj.attr}}")
        self.assertEqual(t.render({'obj': Obj()}), "value")

    def test_method_call(self):
        """Test method calls through dot notation."""
        class Obj:
            def method(self):
                return "method result"

        t = Templite("{{obj.method}}")
        self.assertEqual(t.render({'obj': Obj()}), "method result")

    def test_dict_access(self):
        """Test dictionary access with dots."""
        t = Templite("{{data.key}}")
        self.assertEqual(t.render({'data': {'key': 'value'}}), "value")

    def test_chained_dots(self):
        """Test chained dot access."""
        class Inner:
            def __init__(self):
                self.value = "deep"

        class Outer:
            def __init__(self):
                self.inner = Inner()

        t = Templite("{{obj.inner.value}}")
        self.assertEqual(t.render({'obj': Outer()}), "deep")

    def test_filters(self):
        """Test filter application."""
        t = Templite("{{text|upper}}", {'upper': str.upper})
        self.assertEqual(t.render({'text': 'hello'}), "HELLO")

    def test_chained_filters(self):
        """Test multiple filters in sequence."""
        def double(s):
            return s + s

        t = Templite("{{text|upper|double}}", {'upper': str.upper, 'double': double})
        self.assertEqual(t.render({'text': 'hi'}), "HIHI")

    def test_filter_with_dots(self):
        """Test filters combined with dot notation."""
        def add_exclamation(s):
            return s + "!"

        class Obj:
            def __init__(self):
                self.name = "world"

        t = Templite("{{obj.name|add_exclamation}}", {'add_exclamation': add_exclamation})
        self.assertEqual(t.render({'obj': Obj()}), "world!")

    def test_if_true(self):
        """Test if statement with true condition."""
        t = Templite("{% if condition %}true{% endif %}")
        self.assertEqual(t.render({'condition': True}), "true")

    def test_if_false(self):
        """Test if statement with false condition."""
        t = Templite("{% if condition %}true{% endif %}")
        self.assertEqual(t.render({'condition': False}), "")

    def test_if_with_variables(self):
        """Test if statement with variable interpolation."""
        t = Templite("{% if show %}Hello, {{name}}!{% endif %}")
        self.assertEqual(
            t.render({'show': True, 'name': 'World'}),
            "Hello, World!"
        )
        self.assertEqual(
            t.render({'show': False, 'name': 'World'}),
            ""
        )

    def test_nested_if(self):
        """Test nested if statements."""
        template = """
        {% if outer %}
            Outer is true
            {% if inner %}
                Inner is also true
            {% endif %}
        {% endif %}
        """.strip()
        
        t = Templite(template)
        
        result = t.render({'outer': True, 'inner': True}).strip()
        # Normalize whitespace for comparison
        expected_lines = ["Outer is true", "Inner is also true"] 
        result_lines = [line.strip() for line in result.split('\n') if line.strip()]
        self.assertEqual(result_lines, expected_lines)
        
        result = t.render({'outer': True, 'inner': False}).strip()
        self.assertEqual(result, "Outer is true")
        
        result = t.render({'outer': False, 'inner': True})
        self.assertEqual(result, "")

    def test_for_loop(self):
        """Test simple for loop."""
        t = Templite("{% for item in items %}{{item}} {% endfor %}")
        self.assertEqual(
            t.render({'items': ['a', 'b', 'c']}),
            "a b c "
        )

    def test_for_loop_empty(self):
        """Test for loop with empty list."""
        t = Templite("{% for item in items %}{{item}} {% endfor %}")
        self.assertEqual(t.render({'items': []}), "")

    def test_for_loop_with_filters(self):
        """Test for loop with filters."""
        t = Templite("{% for item in items %}{{item|upper}} {% endfor %}", {'upper': str.upper})
        self.assertEqual(
            t.render({'items': ['a', 'b', 'c']}),
            "A B C "
        )

    def test_nested_for_loops(self):
        """Test nested for loops."""
        template = "{% for row in matrix %}{% for item in row %}{{item}} {% endfor %}| {% endfor %}"
        t = Templite(template)
        matrix = [['a', 'b'], ['c', 'd']]
        self.assertEqual(t.render({'matrix': matrix}), "a b | c d | ")

    def test_for_loop_with_objects(self):
        """Test for loop with object attribute access."""
        class Product:
            def __init__(self, name, price):
                self.name = name
                self.price = price

        def format_price(price):
            return f"${price:.2f}"

        template = "{% for product in products %}{{product.name}}: {{product.price|format_price}} {% endfor %}"
        t = Templite(template, {'format_price': format_price})
        
        products = [Product("Apple", 1.0), Product("Banana", 0.5)]
        result = t.render({'products': products})
        self.assertEqual(result, "Apple: $1.00 Banana: $0.50 ")

    def test_comments(self):
        """Test that comments are ignored."""
        t = Templite("Hello{# this is a comment #} World")
        self.assertEqual(t.render(), "Hello World")

    def test_multiline_comments(self):
        """Test multiline comments."""
        template = """Hello
        {# This is a
           multiline comment #}
        World"""
        t = Templite(template)
        result = t.render()
        self.assertIn("Hello", result)
        self.assertIn("World", result)
        self.assertNotIn("multiline comment", result)

    def test_complex_template(self):
        """Test a complex template combining all features."""
        template = """
        <html>
        <head><title>{{page_title}}</title></head>
        <body>
            <h1>Welcome, {{user.name|title}}!</h1>
            {% if user.is_premium %}
                <p>You are a premium member!</p>
            {% endif %}
            
            <h2>Your Orders:</h2>
            <ul>
            {% for order in orders %}
                <li>Order #{{order.id}}: {{order.total|currency}} 
                    ({{order.items|length}} items)</li>
            {% endfor %}
            </ul>
            
            {# Footer comment #}
            <footer>© 2023 Our Company</footer>
        </body>
        </html>
        """
        
        def currency(amount):
            return f"${amount:.2f}"
        
        def length(items):
            return len(items)
        
        class User:
            def __init__(self, name, is_premium=False):
                self.name = name
                self.is_premium = is_premium
        
        class Order:
            def __init__(self, id, total, items):
                self.id = id
                self.total = total
                self.items = items
        
        t = Templite(template, {
            'title': str.title,
            'currency': currency,
            'length': length
        })
        
        context = {
            'page_title': 'User Dashboard',
            'user': User('john doe', True),
            'orders': [
                Order(101, 25.50, ['item1', 'item2']),
                Order(102, 15.25, ['item3'])
            ]
        }
        
        result = t.render(context)
        
        self.assertIn('User Dashboard', result)
        self.assertIn('Welcome, John Doe!', result)
        self.assertIn('premium member', result)
        self.assertIn('Order #101: $25.50', result)
        self.assertIn('(2 items)', result)
        self.assertNotIn('Footer comment', result)

    def test_constructor_context(self):
        """Test context passed to constructor."""
        t = Templite("{{greeting}}, {{name}}!", {'greeting': 'Hello'})
        self.assertEqual(
            t.render({'name': 'World'}),
            "Hello, World!"
        )

    def test_render_context_overrides(self):
        """Test that render context overrides constructor context."""
        t = Templite("{{value}}", {'value': 'constructor'})
        self.assertEqual(t.render({'value': 'render'}), "render")

    def test_whitespace_handling(self):
        """Test various whitespace scenarios."""
        # Test that whitespace in expressions is handled
        t = Templite("{{ name }}")
        self.assertEqual(t.render({'name': 'test'}), "test")
        
        # Test that whitespace in tags is handled
        t = Templite("{% if condition %}yes{% endif %}")
        self.assertEqual(t.render({'condition': True}), "yes")

    # Error handling tests
    def test_syntax_error_bad_if(self):
        """Test syntax error for malformed if."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% if %}")

    def test_syntax_error_bad_for(self):
        """Test syntax error for malformed for."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% for %}")
        
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% for item %}")
        
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% for item not_in list %}")

    def test_syntax_error_unknown_tag(self):
        """Test syntax error for unknown tags."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% unknown %}")

    def test_syntax_error_unmatched_end(self):
        """Test syntax error for unmatched end tags."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% endif %}")

    def test_syntax_error_wrong_end_tag(self):
        """Test syntax error for wrong end tag."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% if condition %}{% endfor %}")

    def test_syntax_error_unclosed_tag(self):
        """Test syntax error for unclosed tags."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% if condition %}")

    def test_syntax_error_bad_variable_name(self):
        """Test syntax error for bad variable names."""
        with self.assertRaises(TempliteSyntaxError):
            Templite("{{123invalid}}")
        
        with self.assertRaises(TempliteSyntaxError):
            Templite("{% for 123invalid in items %}{% endfor %}")

    def test_attribute_error_handling(self):
        """Test handling of attribute errors in dot notation."""
        class Obj:
            pass
        
        t = Templite("{{obj.missing}}")
        
        # Should try attribute access first, then key access
        obj_with_dict = Obj()
        obj_with_dict.missing = "found"
        self.assertEqual(t.render({'obj': obj_with_dict}), "found")

    def test_key_error_in_dot_access(self):
        """Test key error when neither attribute nor key exists."""
        t = Templite("{{obj.missing}}")
        
        # This should raise an error since neither attribute nor key exists
        with self.assertRaises(KeyError):
            t.render({'obj': {}})


if __name__ == '__main__':
    unittest.main()
