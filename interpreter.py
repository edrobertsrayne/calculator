"""
Parser and Interpreter for an aritmetic calculator.

Uses the following grammatical rules:

Expression: term ((PLUS | MINUS) term)*
Term: factor ((MUL | DIV) factor)*
Factor: atom (POW atom)?
Atom: (PLUS | MINUS) atom | scientific | variable | LPAREN expression RPAREN | function
Scientific: number (E number)?
Function: func ((LPAREN expression RPAREN) | scientific)
Number: (PLUS | MINUS)? value
"""
from lexer import Token, TokenType


class AST:
    pass


class BinaryOperation(AST):
    def __init__(self, left: AST, token: Token, right: AST) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.token = token
        self.operator = token.type


class UnaryOperation(AST):
    def __init__(self, token: Token, child: AST) -> None:
        super().__init__()
        self.child = child
        self.token = token
        self.operator = token.type


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
        operator = node.operator
        if operator == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif operator == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif operator == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif operator == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif operator == TokenType.POW:
            return self.visit(node.left) ** self.visit(node.right)
        elif operator == TokenType.SCI:
            return self.visit(node.left) * (10 ** self.visit(node.right))
        else:
            raise Exception(
                f"No method implemented for binary operator {node.operator}."
            )

    def visit_UnaryOperation(self, node: UnaryOperation):
        operator = node.operator
        if operator == TokenType.PLUS:
            return +self.visit(node.child)
        elif operator == TokenType.MINUS:
            return -self.visit(node.child)
        else:
            raise Exception(
                f"No method implemented for unary operator {node.operator.type}."
            )

    def visit_Number(self, node: Number):
        return node.value
