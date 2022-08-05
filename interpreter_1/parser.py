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
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expression:
        expr = self.term()

        while self.match("LESS_EQUAL", "GREATER_EQUAL", "LESS", "GREATER"):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.primary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match('NIL'):
            return Literal(self.previous().lexeme)
        if self.match('TRUE'):
            return Literal(self.previous().lexeme)
        if self.match('FALSE'):
            return Literal(self.previous().lexeme)
        if self.match("NUMBER"):
            return Literal(int(self.previous().lexeme))
        if self.match("STRING"):
            return Literal(self.previous().lexeme)

        if self.match('LEFT_PAREN'):
            expr = self.expression()
            self.consume('RIGHT_PAREN', "Expect ')' after expression.")
            return Grouping(expr)
        print("did not match:", self.peek())

    def consume(self, token_type, error_message: str):
        if self.check(token_type):
            return self.advance()

        raise Exception(f"{token_type}:, {error_message})")

    def parse(self):
        return self.expression()
