from scanner import Scanner
import sys

def run_interactive_mode():
    while True:
        try:
            line = input("> ")
            # for now just echo the line
            print(line)
        except KeyboardInterrupt:
            print(" Goodbye ...")
            sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        scanner = Scanner(file)
        tokens = scanner.scan_tokens()
        print(tokens)
    else:
        run_interactive_mode()

