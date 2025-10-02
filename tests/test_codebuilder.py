"""Test the CodeBuilder class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from codebuilder import CodeBuilder


class TestCodeBuilder(unittest.TestCase):
    """Test the CodeBuilder class."""

    def test_empty_code(self):
        """Test empty code generation."""
        code = CodeBuilder()
        self.assertEqual(str(code), "")

    def test_single_line(self):
        """Test adding a single line."""
        code = CodeBuilder()
        code.add_line("print('hello')")
        self.assertEqual(str(code), "print('hello')\n")

    def test_multiple_lines(self):
        """Test adding multiple lines."""
        code = CodeBuilder()
        code.add_line("x = 1")
        code.add_line("y = 2")
        self.assertEqual(str(code), "x = 1\ny = 2\n")

    def test_indentation(self):
        """Test indentation management."""
        code = CodeBuilder()
        code.add_line("if True:")
        code.indent()
        code.add_line("print('indented')")
        code.dedent()
        code.add_line("print('not indented')")
        
        expected = "if True:\n    print('indented')\nprint('not indented')\n"
        self.assertEqual(str(code), expected)

    def test_nested_indentation(self):
        """Test nested indentation."""
        code = CodeBuilder()
        code.add_line("if True:")
        code.indent()
        code.add_line("if True:")
        code.indent()
        code.add_line("print('double indented')")
        code.dedent()
        code.add_line("print('single indented')")
        code.dedent()
        code.add_line("print('not indented')")
        
        expected = ("if True:\n"
                   "    if True:\n"
                   "        print('double indented')\n"
                   "    print('single indented')\n"
                   "print('not indented')\n")
        self.assertEqual(str(code), expected)

    def test_initial_indent(self):
        """Test CodeBuilder with initial indentation."""
        code = CodeBuilder(indent=8)
        code.add_line("print('hello')")
        self.assertEqual(str(code), "        print('hello')\n")

    def test_section(self):
        """Test adding a section."""
        code = CodeBuilder()
        code.add_line("# Start")
        section = code.add_section()
        code.add_line("# End")
        
        section.add_line("# Middle")
        
        expected = "# Start\n# Middle\n# End\n"
        self.assertEqual(str(code), expected)

    def test_section_with_indentation(self):
        """Test section with proper indentation."""
        code = CodeBuilder()
        code.add_line("def func():")
        code.indent()
        section = code.add_section()
        code.add_line("return result")
        code.dedent()
        
        # Add to section after indentation is set
        section.add_line("x = 1")
        section.add_line("y = 2")
        
        expected = ("def func():\n"
                   "    x = 1\n"
                   "    y = 2\n"
                   "    return result\n")
        self.assertEqual(str(code), expected)

    def test_get_globals_simple(self):
        """Test executing simple code and getting globals."""
        code = CodeBuilder()
        code.add_line("x = 42")
        code.add_line("def func(): return 'hello'")
        
        globals_dict = code.get_globals()
        self.assertEqual(globals_dict['x'], 42)
        self.assertEqual(globals_dict['func'](), 'hello')

    def test_get_globals_function(self):
        """Test executing a function definition."""
        code = CodeBuilder()
        code.add_line("def add(a, b):")
        code.indent()
        code.add_line("return a + b")
        code.dedent()
        
        globals_dict = code.get_globals()
        add_func = globals_dict['add']
        self.assertEqual(add_func(2, 3), 5)

    def test_get_globals_with_section(self):
        """Test get_globals with sections."""
        code = CodeBuilder()
        code.add_line("def func():")
        code.indent()
        
        # Create section for function body
        body = code.add_section()
        
        code.add_line("return result")
        code.dedent()
        
        # Add to section
        body.add_line("result = 'from section'")
        
        globals_dict = code.get_globals()
        func = globals_dict['func']
        self.assertEqual(func(), 'from section')

    def test_get_globals_indent_check(self):
        """Test that get_globals checks for proper indentation."""
        code = CodeBuilder()
        code.add_line("def func():")
        code.indent()
        code.add_line("return True")
        # Forgot to dedent
        
        with self.assertRaises(AssertionError):
            code.get_globals()


if __name__ == '__main__':
    unittest.main()
