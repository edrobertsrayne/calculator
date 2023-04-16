"""Data types for token management"""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    EOF = auto()
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    DIV = auto()
    MUL = auto()
    LPAREN = auto()
    RPAREN = auto()
    POW = auto()
    MOD = auto()  # TODO: Implement modulus function
    FUNC = auto()
    ID = auto()  # TODO: Implement variables


@dataclass
class Token:
    """class to store tokens Token(type, value)"""

    type: TokenType
    value: Any
