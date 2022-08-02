from scanner import Scanner
from astprinter import AstPrinter
from parser import Parser
import sys

def run_interactive_mode():
    scanner = Scanner('')
    a = AstPrinter()
    while True:
        try:
            line = input("> ")
            scanner.content = line
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expr = parser.parse()
            print(a.print(expr))
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

