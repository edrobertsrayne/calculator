from interpreter import Interpreter, Parser
from lexer import Lexer
import pytest


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
        ("7 + 3 * (10 / (12 / (3 + 1) - 1))", 22),
        ("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)", 10),
        ("7 + (((3 + 2)))", 12),
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
    ],
)
def test_binary_opertations(input_values, expected_output):
    assert interpret(input_values) == expected_output
