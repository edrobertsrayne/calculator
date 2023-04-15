"""
Parser and Interpreter for an aritmetic calculator.

Uses the following grammatical rules:

Expression: term ((PLUS | MINUS) term)*
Term: factor ((MUL | DIV) factor)*
Factor: atom (POW atom)?
Atom: (PLUS | MINUS) atom | scientific | variable | LPAREN expression RPAREN | function
Scientific: number (E number)?
Function: func ((LPAREN expression RPAREN) | scientific)
Number: (PLUS | MINUS)? value
"""
from calculator.ast import *
from calculator.lexer import TokenType
from calculator.parser import Parser


class NodeVisitor:
    """
    Parent class to implement the Visitor pattern.
    https://en.wikipedia.org/wiki/Visitor_pattern
    """

    def __init__(self) -> None:
        pass

    def visit(self, node: AST):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AST):
        raise Exception(f"No visit_{type(node).__name__} method.")


class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser) -> None:
        super().__init__()
        self.parser = parser

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_BinaryOperation(self, node: BinaryOperation):
        operator = node.operator
        if operator == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif operator == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif operator == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif operator == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif operator == TokenType.POW:
            return self.visit(node.left) ** self.visit(node.right)
        elif operator == TokenType.SCI:
            return self.visit(node.left) * (10 ** self.visit(node.right))
        else:
            raise Exception(
                f"No method implemented for binary operator {node.operator}."
            )

    def visit_UnaryOperation(self, node: UnaryOperation):
        operator = node.operator
        if operator == TokenType.PLUS:
            return +self.visit(node.child)
        elif operator == TokenType.MINUS:
            return -self.visit(node.child)
        else:
            raise Exception(
                f"No method implemented for unary operator {node.operator.type}."
            )

    def visit_Number(self, node: Number):
        return node.value
