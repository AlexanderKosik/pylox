from scanner import Scanner
from astprinter import AstPrinter
from parser import Parser
from expressions import *
from statement import *
from typing import List
from environment import Environment
import sys
import numbers

try:
    import atexit
    import readline
    histfile = ".interpreter_history"
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass
except ImportError:
    pass


atexit.register(readline.write_history_file, histfile)

class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def evaluate(self, expr: Expression):
        return expr.accept(self)

    def visitExpressionStmt(self, stmt: Stmt):
        self.evaluate(stmt.expr)

    def visitPrintStmt(self, stmt: Stmt):
        value = self.evaluate(stmt.expr)
        print(value)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expr)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.type == 'BANG':
            return not right
        if expr.operator.type == 'MINUS':
            return -right

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op = expr.operator
        match op.type:
            case 'SLASH':
                return int(left) / int(right)
            case 'STAR':
                return int(left) * int(right)
            case 'MINUS':
                return int(left) - int(right)
            case 'PLUS':
                if isinstance(left, numbers.Number) and isinstance(right, numbers.Number):
                    return int(left) + int(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
                else:
                    raise Exception('Operands must be of same type (number or string)')
            case 'EQUAL_EQUAL':
                return left == right
            case 'BANG_EQUAL':
                return left != right
            case 'LESS_EQUAL':
                return int(left) <= int(right)
            case 'GREATER_EQUAL':
                return int(left) >= int(right)
            case 'LESS':
                return int(left) < int(right)
            case 'GREATER':
                return int(left) > int(right)

    def visitVarStmt(self, stmt: VarStmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name, value)

    def visitVariableExpression(self, variable: Variable):
        return self.environment.get(variable.name)

    def visitAssignment(self, assignment: Assignment):
        value = self.evaluate(assignment.value)
        self.environment.assign(assignment.name, value)
        return value

    def visitBlockStmt(self, statement):
        self.executeBlock(statement.statements, Environment())

    def executeBlock(self, statements, env):
        prev = self.environment
        try:
            self.environment = env
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = prev

    def interpret(self, statements: List[Expression]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except Exception as e:
            print(e)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

def run_interactive_mode():
    scanner = Scanner('')
    interpreter = Interpreter()
    while True:
        try:
            line = input("> ")
            scanner.content = line
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            try:
                statements = parser.parse()
                interpreter.interpret(statements)
            except Exception as e:
                print(e)
        except KeyboardInterrupt:
            print(" Goodbye ...")
            sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        scanner = Scanner.from_file(file)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        interpreter.interpret(statements)
    else:
        run_interactive_mode()

