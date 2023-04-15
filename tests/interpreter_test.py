import pytest

from calculator.interpreter import Interpreter, Parser
from calculator.lexer import Lexer


def interpret(input):
    lexer = Lexer(input)
    parser = Parser(lexer=lexer)
    interpreter = Interpreter(parser=parser)
    result = interpreter.interpret()
    return result


@pytest.mark.parametrize(
    "input_values, expected_output",
    [
        ("1+1", 2),
        ("1+1+1", 3),
        ("3-1", 2),
        ("4+5-2", 7),
        ("3", 3),
        ("2+7*4", 30),
        ("(2+7)*4", 36),
        ("7-8/4", 5),
        ("14+2*3-6/2", 17),
        ("2^2", 4),
        ("3^(1+2)", 27),
        ("2^(2*5)", 1024),
        ("3*2^2", 12),
        ("3^2*2", 18),
        ("-1", -1),
        ("--1", 1),
        ("-+1", -1),
        ("5--2", 7),
        ("5+-2", 3),
        ("5---2", 3),
        ("+2", 2),
        ("2++2", 4),
        ("1.1", 1.1),
        ("1.5*2", 3),
        ("2*3E3", 6000),
        ("2E4*2", 40000),
        ("2E1+2", 22),
        ("3/2", 1.5),
    ],
)
def test_binary_opertations(input_values, expected_output):
    assert interpret(input_values) == expected_output
