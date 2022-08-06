from scanner import Scanner
from astprinter import AstPrinter
from parser import Parser
from expressions import *
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
    def evaluate(self, expr: Expression):
        return expr.accept(self)

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

    def interpret(self, expr: Expression):
        try:
            value = self.evaluate(expr)
            print(str(value))
        except Exception as e:
            raise
        #prinr(e)

def run_interactive_mode():
    scanner = Scanner('')
    interpreter = Interpreter()
    while True:
        try:
            line = input("> ")
            scanner.content = line
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expr = parser.parse()
            interpreter.interpret(expr)
        except KeyboardInterrupt:
            print(" Goodbye ...")
            sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        scanner = Scanner.from_file(file)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expr = parser.parse()
        AstPrinter().print(expr)
    else:
        run_interactive_mode()

