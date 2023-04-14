"""
Parser and Interpreter for an aritmetic calculator.

Uses the following grammatical rules:

Expression: term ((PLUS | MINUS) term)*
Term: factor ((MUL | DIV) factor)*
Factor: atom (POW expression)?
Atom: scientific | variable | LPAREN expression RPAREN | function
Scientific: number (E number)?
Function: func ((LPAREN expression RPAREN) | scientific)

"""
from lexer import TokenType, Token
import logging


class Interpreter:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self._get_next_token()

    def run(self):
        return self.expression()

    def _get_next_token(self):
        self.current_token = next(self.lexer, Token(TokenType.EOF, None))

    def check_token(self, token_type):
        """If the token type matches the expected type, fetch the next token. Otherwise raise an error"""
        if self.current_token.type == token_type:
            self._get_next_token()
        else:
            raise ValueError(
                f"Invalid syntax: expected {token_type} but recieved {self.current_token}"
            )

    def factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.check_token(TokenType.NUMBER)
            return token.value
        elif token.type == TokenType.LPAREN:
            self.check_token(TokenType.LPAREN)
            result = self.expression()
            self.check_token(TokenType.RPAREN)
            return result
        else:
            raise ValueError(f"Invalid syntax: {token}")

    def term(self):
        result = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            if self.current_token.type == TokenType.MUL:
                self.check_token(TokenType.MUL)
                result *= self.term()
            elif self.current_token.type == TokenType.DIV:
                self.check_token(TokenType.DIV)
                result /= self.term()
        return result

    def expression(self):
        result = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.check_token(TokenType.PLUS)
                result += self.term()
            elif self.current_token.type == TokenType.MINUS:
                self.check_token(TokenType.MINUS)
                result -= self.term()
        return result
