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


class AST:
    pass


class BinaryOperation(AST):
    def __init__(self, left: AST, operator: Token, right: AST) -> None:
        super().__init__()
        self.left = left
        self.token = self.operator = operator
        self.right = right


class Number(AST):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.token = token
        self.value = token.value


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

    def factor(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.check_token(TokenType.NUMBER)
            return Number(token)
        elif token.type == TokenType.LPAREN:
            self.check_token(TokenType.LPAREN)
            node = self.expression()
            self.check_token(TokenType.RPAREN)
            return node
        else:
            raise ValueError(f"Invalid syntax: {token}")

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.check_token(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.check_token(TokenType.DIV)
            node = BinaryOperation(left=node, operator=token, right=self.factor())
        return node

    def expression(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.check_token(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.check_token(TokenType.MINUS)
            node = BinaryOperation(left=node, operator=token, right=self.term())
        return node


class NodeVisitor:
    """
    Parent class to implement the Visitor pattern.
    https://en.wikipedia.org/wiki/Visitor_pattern
    """

    def __init__(self) -> None:
        pass

    def visit(self, node: AST):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AST):
        raise Exception(f"No visit_{type(node).__name__} method.")


class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser) -> None:
        super().__init__()
        self.parser = parser

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_BinaryOperation(self, node: BinaryOperation):
        if node.operator.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.operator.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.operator.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.operator.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        else:
            raise Exception(f"No method implemented for {node.operator}.")

    def visit_Number(self, node: Number):
        return node.value
