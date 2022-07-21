from scanner import Scanner
import sys

def run_interactive_mode():
    scanner = Scanner('')
    while True:
        try:
            line = input("> ")
            scanner.content = line
            tokens = scanner.scan_tokens()
            print(tokens)
        except KeyboardInterrupt:
            print(" Goodbye ...")
            sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        scanner = Scanner.from_file(file)
        tokens = scanner.scan_tokens()
        print(tokens)
    else:
        run_interactive_mode()

