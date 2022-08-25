from expressions import Expression
from loxtoken import LoxToken
from typing import List

class Stmt:
    """
    Statement base class
    """
    pass

class ExpressionStmt(Stmt):
    def __init__(self, expr: Expression):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        visitor.visitExpressionStmt(self)

class PrintStmt(Stmt):
    def __init__(self, expr: Expression):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        visitor.visitPrintStmt(self)

class VarStmt(Stmt):
    def __init__(self, name: LoxToken, initializer: Expression):
        self.name = name.lexeme
        self.initializer = initializer

    def accept(self, visitor):
        visitor.visitVarStmt(self)

class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def accept(self, visitor):
        visitor.visitBlockStmt(self)

