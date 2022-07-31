from expressions import *

class AstPrinter:
    def print(self, expr: Expression) -> str:
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary) -> str:
        return f'({expr.operator.lexeme}, {expr.left.accept(self)}, {expr.right.accept(self)})'

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return f'(group, {expr.expr.accept(self)})'

    def visitUnary(self, expr: Unary) -> str:
        return f'( {expr.operator.lexeme}, {expr.right.accept(self)})'

    def visitLiteral(self, expr: Literal) -> str:
        if expr.value is None:
            return 'nil'
        return str(expr.value)
