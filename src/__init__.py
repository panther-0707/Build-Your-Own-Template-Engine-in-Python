"""Templite: A Simple Template Engine

A lightweight template engine implementation in Python.
Based on the "500 Lines or Less" book chapter by Ned Batchelder.

Usage:
    from templite import Templite
    
    # Create a template
    template = Templite('''
        <h1>Hello {{name|upper}}!</h1>
        {% for topic in topics %}
            <p>You are interested in {{topic}}.</p>
        {% endfor %}
    ''', {'upper': str.upper})
    
    # Render with data
    result = template.render({
        'name': 'World',
        'topics': ['Python', 'Templates', 'Programming']
    })
"""

# Handle both package imports and direct imports
try:
    from .templite import Templite
    from .exceptions import TempliteSyntaxError
    from .codebuilder import CodeBuilder
except ImportError:
    from templite import Templite
    from exceptions import TempliteSyntaxError
    from codebuilder import CodeBuilder

__version__ = "1.0.0"
__author__ = "Based on Ned Batchelder's implementation"

__all__ = ['Templite', 'TempliteSyntaxError', 'CodeBuilder']
