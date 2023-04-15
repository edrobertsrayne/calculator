"""lexer to tokenize input strings"""

from calculator.token import Token, TokenType


class Lexer:
    """Create an iterator to tokenize an input string"""

    def __init__(self, text) -> None:
        self.text = text.upper()
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
            if self._current_char == "^":
                self._advance()
                return Token(TokenType.POW, "^")
            if self._current_char == "(":
                self._advance()
                return Token(TokenType.LPAREN, "(")
            if self._current_char == ")":
                self._advance()
                return Token(TokenType.RPAREN, ")")
            if self._current_char == "E":
                self._advance()
                return Token(TokenType.SCI, "E")
            self._error()
        # EOF reached: reset pointer and stop iteraction
        self._pos = 0
        raise StopIteration

    def _number(self) -> int:
        buffer = ""

        while self._current_char is not None and self._current_char.isdigit():
            buffer += self._current_char
            self._advance()
        if self._current_char == ".":
            buffer += self._current_char
            self._advance()
            while self._current_char is not None and self._current_char.isdigit():
                buffer += self._current_char
                self._advance()
            return float(buffer)
        else:
            return int(buffer)

    def _skip_whitespace(self) -> None:
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _error(self) -> None:
        """Handle errors"""
        raise ValueError(f"Invalid character: {self._current_char}")

    def _advance(self) -> None:
        """Advance the position pointer and update the current character"""
        self._pos += 1
        if self._pos < len(self.text):
            self._current_char = self.text[self._pos]
        else:
            self._current_char = None
