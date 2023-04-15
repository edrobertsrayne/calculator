from dataclasses import dataclass
from enum import Enum
from typing import Any

TokenType = Enum(
    "TokenType",
    ["EOF", "NUMBER", "PLUS", "MINUS", "DIV", "MUL", "LPAREN", "RPAREN", "POW", "SCI"],
)


@dataclass
class Token:
    """class to store tokens Token(type, value)"""

    type: TokenType
    value: Any
