"""Interpreter class"""
from typing import Any

from calculator.ast import AST, BinaryOperation, Number, UnaryOperation
from calculator.lexer import TokenType
from calculator.parser import Parser


class NodeVisitor:  # pylint: disable=too-few-public-methods
    """
    Parent class to implement the Visitor pattern.

    https://en.wikipedia.org/wiki/Visitor_pattern
    """

    def __init__(self) -> None:
        pass

    def visit(self, node: AST):
        """Method to trawl the AST tree.

        Requires a 'vist_' method for each type of node defined.
        Raises a RunTimeError if no visit method found.
        """
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: AST):
        raise RuntimeError(f"No visit_{type(node).__name__} method.")


class Interpreter(NodeVisitor):
    """Class to represent an interpreter"""

    def __init__(self, parser: Parser) -> None:
        super().__init__()
        self.parser: Parser = parser

    def interpret(self) -> Any:
        """Method to interpret an AST tree"""
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_BinaryOperation(
        self, node: BinaryOperation
    ):  # pylint: disable=invalid-name
        """Visit method for BinaryOperation nodes."""
        operator = node.operator
        if operator == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if operator == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if operator == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        if operator == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        if operator == TokenType.POW:
            return self.visit(node.left) ** self.visit(node.right)
        raise RuntimeError(
            f"No method implemented for binary operator {node.operator}."
        )

    def visit_UnaryOperation(
        self, node: UnaryOperation
    ):  # pylint: disable=invalid-name
        """Visit method for UnaryOperation nodes."""
        operator = node.operator
        if operator == TokenType.PLUS:
            return +self.visit(node.child)
        if operator == TokenType.MINUS:
            return -self.visit(node.child)
        raise RuntimeError(f"No method implemented for unary operator {node.operator}.")

    def visit_Number(self, node: Number):  # pylint: disable=invalid-name
        """Visit method for Number nodes."""
        return node.value
