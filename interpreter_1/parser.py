from expressions import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.current = self.tokens[self.idx]

    def match(self, *token_types) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def peek(self):
        return self.tokens[self.idx]

    def isAtEnd(self):
        return self.match("EOF")

    def check(self, token_type) -> bool:
        return self.peek().type == token_type

    def previous(self):
        return self.tokens[self.idx - 1]

    def advance(self):
        if not self.isAtEnd():
            self.idx += 1
        return self.previous()

    def expression(self) -> Expression:
        return self.equality()

    def equality(self) -> Expression:
        expr = self.comparison()

        while self.match("EQUAL_EQUAL", "BANG_EQUAL"):
            operator = self.previous()
            right = comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expression:
        expr = self.literal()
        return expr

    def literal(self):
        if self.match('NUMBER', 'STRING'):
            return Literal(self.previous().lexeme)
        print("did not match:", self.peek())

    def parse(self):
        return self.expression()
