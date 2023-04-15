from calculator.ast import *
from calculator.token import Token, TokenType


class Parser:
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.current_token = next(self.lexer)

    def parse(self):
        return self.expression()

    def check_token(self, token_type):
        """If the token type matches the expected type, fetch the next token. Otherwise raise an error"""
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
            self.check_token(TokenType.PLUS)
            return UnaryOperation(token=token, child=self.number())
        elif token.type == TokenType.MINUS:
            self.check_token(TokenType.MINUS)
            return UnaryOperation(token=token, child=self.number())
        elif token.type == TokenType(TokenType.NUMBER):
            self.check_token(TokenType.NUMBER)
            return Number(token)
        else:
            raise Exception("Synatax error: expected a number.")

    def scientific(self):
        """Scientific: number (E number)?"""
        node = self.number()
        token = self.current_token
        if token.type == TokenType.SCI:
            self.check_token(TokenType.SCI)
            node = BinaryOperation(left=node, token=token, right=self.number())
        return node

    def atom(self):
        """Atom: (PLUS | MINUS) atom | scientific | variable | LPAREN expression RPAREN | function"""
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.check_token(TokenType.PLUS)
            node = UnaryOperation(token, self.atom())
            return node
        elif token.type == TokenType.MINUS:
            self.check_token(TokenType.MINUS)
            node = UnaryOperation(token, self.atom())
            return node
        elif token.type == TokenType.NUMBER:
            # return self.scientific()
            return self.number()
        elif token.type == TokenType.LPAREN:
            self.check_token(TokenType.LPAREN)
            node = self.expression()
            self.check_token(TokenType.RPAREN)
            return node
        else:
            raise ValueError(f"Invalid syntax: {token}")

    def factor(self):
        """Factor: atom (POW atom)?"""
        node = self.atom()
        token = self.current_token
        if token.type == TokenType.POW:
            self.check_token(TokenType.POW)
            node = BinaryOperation(left=node, token=token, right=self.atom())
        return node

    def term(self):
        """Term: factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.check_token(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.check_token(TokenType.DIV)
            node = BinaryOperation(left=node, token=token, right=self.factor())
        return node

    def expression(self):
        """Expression: term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.check_token(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.check_token(TokenType.MINUS)
            node = BinaryOperation(left=node, token=token, right=self.term())
        return node
