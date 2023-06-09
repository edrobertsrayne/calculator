"""Test suite for the lexer module"""
import pytest

from calculator.lexer import Lexer, Token, TokenType


def test_lexer_advance_position():
    """Ensure that the lexer advances the position pointer correctly after each read"""
    lexer = Lexer("test")
    lexer._advance()
    lexer._advance()
    assert lexer._pos == 2


def test_lexer_advance_current_character():
    """Ensure that the lexer reads the correctly capitalised character when it advances"""
    lexer = Lexer("test")
    lexer._advance()
    assert lexer._current_char == "E"


def test_lexer_does_not_overflow():
    """Return None if lexer advances beyond the end of the input string"""
    lexer = Lexer("t")
    lexer._advance()
    assert lexer._current_char is None


def test_lexer_stops_iteration():
    lexer = Lexer("1")
    next(lexer)
    with pytest.raises(StopIteration):
        next(lexer)


def test_lexer_invalid_character():
    """Ensure that lexer raises a ValueError on invalid characters"""
    with pytest.raises(ValueError):
        list(Lexer("#"))


@pytest.mark.parametrize(
    "input", ["1e1", "1.0e2", "2e-1", "1e100", "0.1e10", "2e-100", ".1E14"]
)
def test_lexer_scientific(input):
    lexer = Lexer(input)
    assert next(lexer).value == float(input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "2 - 3",
            [
                Token(TokenType.NUMBER, 2),
                Token(TokenType.MINUS, "-"),
                Token(TokenType.NUMBER, 3),
            ],
        ),
        (
            "10 + 1",
            [
                Token(TokenType.NUMBER, 10),
                Token(TokenType.PLUS, "+"),
                Token(TokenType.NUMBER, 1),
            ],
        ),
        (
            "1 + 1",
            [
                Token(TokenType.NUMBER, 1),
                Token(TokenType.PLUS, "+"),
                Token(TokenType.NUMBER, 1),
            ],
        ),
        (
            "1 / 1",
            [
                Token(TokenType.NUMBER, 1),
                Token(TokenType.DIV, "/"),
                Token(TokenType.NUMBER, 1),
            ],
        ),
        (
            "1 * 1",
            [
                Token(TokenType.NUMBER, 1),
                Token(TokenType.MUL, "*"),
                Token(TokenType.NUMBER, 1),
            ],
        ),
    ],
)
def test_lexer(test_input, expected):
    """Test that the lexer is correctly tokenizing strings"""
    assert list(Lexer(test_input)) == expected
