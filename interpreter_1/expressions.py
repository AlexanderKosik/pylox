from loxtoken import LoxToken

class Expression:
    """ Base class for all expressions
    """

class Binary(Expression):
    def __init__(self, left: Expression, operator: LoxToken, right: Expression):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expression):
    def __init__(self, expr: Expression):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteral(self)


class Unary(Expression):
    def __init__(self, operator: LoxToken, right: Expression):
        super().__init__()
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnary(self)


if __name__ == '__main__':
    un = Unary(operator=LoxToken('MINUS', '-', None, 1), right=Literal(42))
    from astprinter import AstPrinter
    a = AstPrinter()
    print(a.print(un))