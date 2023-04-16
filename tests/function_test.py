import math

import pytest
from pytest import approx

from calculator.ast import Function, Number
from calculator.interpreter import Interpreter
from calculator.lexer import Lexer
from calculator.parser import Parser
from calculator.token import Token, TokenType


@pytest.mark.parametrize(
    "input_text", [("cos2"), ("cos(45)"), ("cos-45"), ("cos(-13)")]
)
def test_lexer_function_token_type(input_text):
    lexer = Lexer(input_text)
    assert next(lexer).type == TokenType.FUNC


@pytest.mark.parametrize(
    "input_text, function_name",
    [
        ("cos(45)", "COS"),
        ("cos45", "COS"),
        ("sin(45)", "SIN"),
        ("sin45", "SIN"),
        ("tan(45)", "TAN"),
        ("tan45", "TAN"),
    ],
)
def test_lexer_function_token_value(input_text, function_name):
    lexer = Lexer(input_text)
    assert next(lexer).value == function_name


def test_parser_simple_function_tree():
    lexer = Lexer("cos(45)")
    parser = Parser(lexer)
    tree = parser.parse()

    number_node = Number(Token(TokenType.NUMBER, 45))
    expected_tree = Function(Token(TokenType.FUNC, "COS"), number_node)

    assert tree.token.__dict__ == expected_tree.token.__dict__
    assert tree.child.__dict__ == expected_tree.child.__dict__


@pytest.mark.parametrize(
    "input_string, expected_value",
    [
        ("cos(45)", math.cos(math.radians(45))),
        ("sin(30)", math.sin(math.radians(30))),
        ("tan60", math.tan(math.radians(60))),
        ("exp(4+9)", math.exp(13)),
        ("ln4", math.log(4)),
        ("log100", math.log10(100)),
        ("sqrt25", 5),
        ("acos0.5", 60),
        ("asin(1/2)", 30),
        ("atan(1)", 45),
    ],
)
def test_interpreter_simple_function(input_string, expected_value):
    lexer = Lexer(input_string)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    assert result == approx(expected_value)
