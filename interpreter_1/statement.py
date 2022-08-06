from expressions import Expression

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
