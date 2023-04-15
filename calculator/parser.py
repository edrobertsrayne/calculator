"""
Parser for an arithmetic calculator.

Uses the following grammatical rules:

Expression: term ((PLUS | MINUS) term)*
Term: factor ((MUL | DIV) factor)*
Factor: atom (POW atom)?
Atom: (PLUS | MINUS) atom | number | variable | LPAREN expression RPAREN | function
Function: func ((LPAREN expression RPAREN) | number)
Number: (PLUS | MINUS)? value
"""

from calculator.ast import AST, BinaryOperation, Number, UnaryOperation
from calculator.lexer import Lexer
from calculator.token import Token, TokenType


class Parser:
    """Class to implement the parser.

    parser = Parse(Lexer)
    tree = parser.parse()

    Takes a Lexer object or an iterable of tokens as a parameter.
    Returns a tree of AST nodes.
    """

    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.current_token: Token = next(self.lexer)

    def parse(self) -> AST:
        """Method to parse the token stream into an AST tree"""
        return self.expression()

    def _eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = next(self.lexer, Token(TokenType.EOF, None))
        else:
            raise ValueError(
                f"Invalid syntax: expected {token_type} but recieved {self.current_token}"
            )

    def number(self):
        """Number: (PLUS | MINUS)? value"""
        token = self.current_token
        if token.type == TokenType.PLUS:
            self._eat(TokenType.PLUS)
            return UnaryOperation(token=token, child=self.number())
        if token.type == TokenType.MINUS:
            self._eat(TokenType.MINUS)
            return UnaryOperation(token=token, child=self.number())
        if token.type == TokenType(TokenType.NUMBER):
            self._eat(TokenType.NUMBER)
            return Number(token)
        raise SyntaxError("Expected a number.")

    def atom(self):
        """Atom: (PLUS | MINUS) atom
        | number
        | variable
        | LPAREN expression RPAREN
        | function"""
        token = self.current_token
        if token.type == TokenType.PLUS:
            self._eat(TokenType.PLUS)
            node = UnaryOperation(token, self.atom())
            return node
        if token.type == TokenType.MINUS:
            self._eat(TokenType.MINUS)
            node = UnaryOperation(token, self.atom())
            return node
        if token.type == TokenType.NUMBER:
            # return self.scientific()
            return self.number()
        if token.type == TokenType.LPAREN:
            self._eat(TokenType.LPAREN)
            node = self.expression()
            self._eat(TokenType.RPAREN)
            return node
        raise ValueError(f"Invalid syntax: {token}")

    def factor(self):
        """Factor: atom (POW atom)?"""
        node = self.atom()
        token = self.current_token
        if token.type == TokenType.POW:
            self._eat(TokenType.POW)
            node = BinaryOperation(left=node, token=token, right=self.atom())
        return node

    def term(self):
        """Term: factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self._eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self._eat(TokenType.DIV)
            node = BinaryOperation(left=node, token=token, right=self.factor())
        return node

    def expression(self):
        """Expression: term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self._eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self._eat(TokenType.MINUS)
            node = BinaryOperation(left=node, token=token, right=self.term())
        return node
