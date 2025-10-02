"""
An advanced expression parser for the Templite template engine.

This implementation uses a Pratt parser to handle operator precedence.
"""

import re

class ExpressionParser:
    """
    Parses complex expressions with operator precedence, comparisons, and logic.
    """
    def __init__(self, text, templite):
        self.templite = templite
        self.tokens = self._tokenize(text)
        self.pos = 0

    def _tokenize(self, text):
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),
            ('STRING',   r'"[^"]*"'),
            ('LOGIC',    r'\b(and|or|not)\b'),
            ('ID',       r'[_a-zA-Z][_a-zA-Z0-9]*'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('DOT',      r'\.'),
            ('COMP',     r'==|!=|<=|>=|<|>'),
            ('OP',       r'[+\-*/%]'),
            ('SKIP',     r'[ \t]+'),
            ('PIPE',     r'\|'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise ValueError(f"Unexpected character: {value}")
            tokens.append((kind, value))
        tokens.append(('EOF', 'EOF'))
        return tokens

    def parse(self):
        expr = self.parse_expression(0)
        self.match('EOF')
        return expr

    def parse_expression(self, rbp):
        left = self.nud()
        while rbp < self.current_token_bp():
            left = self.led(left)
        return left

    def nud(self):
        """Null denotation: for prefixes and atoms."""
        token_kind, token_value = self.peek()
        self.advance()

        if token_kind == 'NUMBER':
            return token_value
        elif token_kind == 'STRING':
            return token_value
        elif token_kind == 'ID':
            if self.peek()[0] == 'LPAREN':
                return self.handle_function_call(token_value)

            self.templite._variable(token_value, self.templite.all_vars)
            code = f"c_{token_value}"
            return code
        elif token_kind == 'LPAREN':
            expr = self.parse_expression(0)
            self.match('RPAREN')
            return f"({expr})"
        elif token_value == 'not':
            expr = self.parse_expression(70)
            return f"(not {expr})"
        else:
            raise self.templite._syntax_error("Invalid expression start", token_value)

    def led(self, left):
        """Left denotation: for infix and postfix operators."""
        token_kind, token_value = self.peek()

        if token_kind in ('OP', 'COMP', 'LOGIC'):
            bp = self.binding_power(token_value)
            self.advance()
            right = self.parse_expression(bp)
            op = token_value
            return f"({left} {op} {right})"
        elif token_kind == 'DOT':
            self.advance()
            prop = self.peek()[1]
            self.advance()
            return f"do_dots({left}, '{prop}')"
        elif token_kind == 'PIPE':
            self.advance()
            filt = self.peek()[1]
            self.advance()
            self.templite._variable(filt, self.templite.all_vars)
            return f"c_{filt}({left})"
        else:
            raise self.templite._syntax_error("Invalid operator", token_value)

    def handle_function_call(self, name):
        self.advance()
        args = []
        while self.peek()[0] != 'RPAREN':
            args.append(self.parse_expression(0))
            if self.peek()[0] == ',':
                self.advance()
        self.match('RPAREN')
        self.templite._variable(name, self.templite.all_vars)
        return f"c_{name}({', '.join(args)})"

    def current_token_bp(self):
        _, token_value = self.peek()
        return self.binding_power(token_value)

    def binding_power(self, op):
        if op == '.':
            return 80
        if op == 'not':
            return 70
        if op == '|':
            return 60
        if op in ('*', '/', '%'):
            return 50
        if op in ('+', '-'):
            return 40
        if op in ('==', '!=', '<', '<=', '>', '>='):
            return 30
        if op == 'and':
            return 20
        if op == 'or':
            return 10
        return 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        return self.tokens[self.pos - 1]

    def match(self, expected_kind):
        token_kind, _ = self.peek()
        if token_kind == expected_kind:
            return self.advance()
        raise self.templite._syntax_error(f"Expected {expected_kind}", self.peek()[1])