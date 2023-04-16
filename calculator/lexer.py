"""lexer to tokenize input strings"""

from calculator.token import Token, TokenType

BUILTIN_FUNCTIONS = [
    "SIN",
    "COS",
    "TAN",
    "EXP",
    "LN",
    "LOG",
    "SQRT",
    "ACOS",
    "ASIN",
    "ATAN",
]


class Lexer:
    """Create an iterator to tokenize an input string."""

    def __init__(self, text) -> None:
        self.text = text.upper()
        self._pos = 0
        self._current_char = self.text[self._pos]

    def __iter__(self) -> object:
        return self

    def __next__(self) -> Token:
        # TODO: Refactor to reduce the number of return statements
        while self._current_char is not None:
            if self._current_char.isspace():
                self._skip_whitespace()
                continue
            if self._current_char.isdigit() or self._current_char == ".":
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
            if self._current_char.isalpha():
                token = self._read_text()
                return token
            raise ValueError(f"Invalid character: {self._current_char}")

        # EOF reached: reset pointer and stop iteraction
        self._pos = 0
        raise StopIteration

    def _read_text(self) -> Token:
        buffer = ""

        # keep reading all alphabetic characters
        while self._current_char is not None and self._current_char.isalpha():
            buffer += self._current_char
            self._advance()

        # test to see if the buffer represents a builtin function
        if buffer in BUILTIN_FUNCTIONS:
            return Token(TokenType.FUNC, buffer)

        # temporary error
        raise ValueError(f"{buffer} is not a recognized function.")

    def _number(self) -> float:
        buffer = ""

        # keep reading until all digits are captured
        while self._current_char is not None and self._current_char.isdigit():
            buffer += self._current_char
            self._advance()

        # check for decimals
        if self._current_char == ".":
            buffer += self._current_char
            self._advance()
            while self._current_char is not None and self._current_char.isdigit():
                buffer += self._current_char
                self._advance()

        # check for scientific notation
        if self._current_char == "E":
            buffer += self._current_char
            self._advance()
            # catch negative powers
            if self._current_char == "-":
                buffer += self._current_char
                self._advance()
            while self._current_char is not None and self._current_char.isdigit():
                buffer += self._current_char
                self._advance()

        # if the number is an integer, return an integer value
        number = float(buffer)
        return int(number) if number.is_integer() else number

    def _skip_whitespace(self) -> None:
        while self._current_char is not None and self._current_char.isspace():
            self._advance()

    def _advance(self) -> None:
        self._pos += 1
        if self._pos < len(self.text):
            self._current_char = self.text[self._pos]
        else:
            self._current_char = None
