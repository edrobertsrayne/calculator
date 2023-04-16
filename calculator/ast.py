"""Provides classes need to implement an abstract syntax tree"""
from calculator.token import Token


class AST:  # pylint: disable=too-few-public-methods
    """Abstract Syntax Tree parent class."""


class BinaryOperation(AST):  # pylint: disable=too-few-public-methods
    """Class to provide a node for binary operations."""

    def __init__(self, left: AST, token: Token, right: AST) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.token = token
        self.operator = token.type


class UnaryOperation(AST):  # pylint: disable=too-few-public-methods
    """Class to provide a node for unary operations."""

    def __init__(self, token: Token, child: AST) -> None:
        super().__init__()
        self.child = child
        self.token = token
        self.operator = token.type


class Number(AST):  # pylint: disable=too-few-public-methods:
    """Class to provide a node for numbers."""

    def __init__(self, token: Token) -> None:
        super().__init__()
        self.token = token
        self.value = token.value


class Function(AST):
    """Class to provide a node for functions."""

    def __init__(self, token: Token, child: AST) -> None:
        super().__init__()
        self.child = child
        self.token = token
        self.function = token.value
