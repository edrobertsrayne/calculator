from calculator.interpreter import Interpreter
from calculator.lexer import Lexer
from calculator.parser import Parser

while True:
    try:
        text = input("calc> ")  # pylint:disable=bad-builtin
    except EOFError:
        break
    if not text:
        break

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    results = interpreter.interpret()
    print(results)
