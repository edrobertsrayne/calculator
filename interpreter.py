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
            raise ValueError("Invalid syntax. Token does not match.")

    def term(self):
        """term: INTEGER"""
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.check_token(TokenType.NUMBER)
            return token.value
        else:
            raise ValueError("Invalid sytanx. Expected a number.")

    def expression(self):
        """expression: term ((PLUS | MINUS) term)*"""
        result = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.check_token(TokenType.PLUS)
                result += self.term()
            elif self.current_token.type == TokenType.MINUS:
                self.check_token(TokenType.MINUS)
                result -= self.term()
        return result
