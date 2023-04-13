from interpreter import Interpreter
from lexer import Lexer
import pytest


@pytest.mark.parametrize(
    "input_values, expected_output",
    [("1+1", 2), ("1+1+1", 3), ("3-1", 2), ("4+5-2", 7)],
)
def test_addition_and_subtraction(input_values, expected_output):
    interpreter = Interpreter(Lexer(input_values))
    assert interpreter.run() == expected_output
