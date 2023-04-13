"""lexer to tokenize input strings"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

TokenType = Enum("TokenType", ["EOF", "NUMBER", "PLUS", "MINUS", "DIV", "MUL"])


@dataclass
class Token:
    """class to store tokens Token(type, value)"""

    type: TokenType
    value: Any


class Lexer:
    """Create an iterator to tokenize an input string"""

    def __init__(self, text) -> None:
        self.text = text
        self._pos = 0
        self._current_char = self.text[self._pos]

    def __iter__(self) -> object:
        return self

    def __next__(self) -> Token:
        while self._current_char is not None:
            if self._current_char.isspace():
                self._skip_whitespace()
                continue
            if self._current_char.isdigit():
                number = self._number()
                return Token(TokenType.NUMBER, number)
            if self._current_char == "+":
                self._advance()
                return Token(TokenType.PLUS, "+")
            if self._current_char == "-":
                self._advance()
                return Token(TokenType.MINUS, "-")
            if self._current_char == "/":
                self._advance()
                return Token(TokenType.DIV, "/")
            if self._current_char == "*":
                self._advance()
                return Token(TokenType.MUL, "*")
            self._error()
        # EOF reached: reset pointer and stop iteraction
        self._pos = 0
        raise StopIteration

    def _number(self) -> int:
        buffer = ""
        while self._current_char is not None and self._current_char.isdigit():
            buffer += self._current_char
            self._advance()
        return int(buffer)

    def _skip_whitespace(self) -> None:
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _error(self) -> None:
        """Handle errors"""
        raise ValueError("Invalid character")

    def _advance(self) -> None:
        """Advance the position pointer and update the current character"""
        self._pos += 1
        if self._pos < len(self.text):
            self._current_char = self.text[self._pos]
        else:
            self._current_char = None
