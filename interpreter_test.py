from interpreter import Interpreter
from lexer import Lexer
import pytest


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
    ],
)
def test_addition_and_subtraction(input_values, expected_output):
    interpreter = Interpreter(Lexer(input_values))
    assert interpreter.run() == expected_output
