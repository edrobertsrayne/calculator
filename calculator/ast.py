from calculator.token import Token


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
