"""lexer to tokenize input strings"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

TokenType = Enum("TokenType", ["NUMBER", "PLUS"])


@dataclass
class Token:
    """class to store tokens Token(type, value)"""

    type: TokenType
    value: Any


class Lexer:
    """Create an iterator to tokenize an input string"""

    def __init__(self, text) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def __iter__(self):
        return self

    def __next__(self):
        while self.current_char is not None:
            if self.current_char.isdigit():
                number = int(self.current_char)
                self.advance()
                return Token(TokenType.NUMBER, number)
            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")
            self.error()
        raise StopIteration

    def error(self):
        """Handle errors"""

    def advance(self):
        """Advance the position pointer and update the current character"""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
