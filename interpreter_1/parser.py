from expressions import *
from statement import *


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
        return self.peek().type == "EOF"

    def check(self, token_type) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == token_type

    def previous(self):
        return self.tokens[self.idx - 1]

    def advance(self):
        if not self.isAtEnd():
            self.idx += 1
        return self.previous()

    def declaration(self) -> Stmt:
        try:
            if self.match("VAR"):
                return self.varDeclaration()

            return self.statement()
        except Exception as e:
            raise

    def varDeclaration(self):
        name = self.consume("IDENTIFIER", "Expect variable name")

        initializer = None
        if self.match("EQUAL"):
            initializer = self.expression()

        self.consume("SEMICOLON", 'Expect ";" after variable declaration')
        return VarStmt(name, initializer)

    def statement(self) -> Stmt:
        if self.match("LEFT_PAREN"):
            return self.ifStatement()
        if self.match("PRINT"):
            return self.printStatement()
        if self.match("LEFT_BRACE"):
            return Block(self.block())

        return self.expressionStatement()

    
    def block(self):
        statements = []
        while not self.check("RIGHT_BRACE") and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume("RIGHT_BRACE", "Expect '}' after block.")
        return statements

    def ifStatement(self):
        consume("LEFT_PAREN", "Expect '(' after 'if'.")
        condition = self.expression()
        consume("RIGHT_PAREN", "Expect ')' after condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match("ELSE"):
            elseBranch = self.statement()
        return IfStmt(condition, thenBranch, elseBranch)

    def printStatement(self):
        value = self.expression()
        self.consume("SEMICOLON", "Expect ';' after value.")
        return PrintStmt(value)

    def expressionStatement(self):
        expr = self.expression()
        self.consume("SEMICOLON", "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def assignment(self) -> Expression:
        expr = self.equality() 

        if self.match("EQUAL"):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, value)

            raise Exception("Invalid assignment target.")
        
        return expr


    def expression(self) -> Expression:
        return self.assignment()


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
        if self.match("NIL"):
            return Literal(self.previous().lexeme)
        if self.match("TRUE"):
            return Literal(self.previous().lexeme)
        if self.match("FALSE"):
            return Literal(self.previous().lexeme)
        if self.match("NUMBER"):
            return Literal(int(self.previous().lexeme))
        if self.match("STRING"):
            return Literal(self.previous().lexeme)
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return Grouping(expr)
        if self.match("IDENTIFIER"):
            return Variable(self.previous())

        print("did not match:", self.peek())

    def consume(self, token_type, error_message: str):
        if self.check(token_type):
            return self.advance()

        raise Exception(f"{token_type}:, {error_message}")

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
