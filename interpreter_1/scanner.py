from loxtoken import LoxToken

class Scanner:
    def __init__(self, source_file):
        self.source_file = source_file
        self.single_char_tokens = {
            # character: token_type
            '(': 'LEFT_PAREN',
            ')': 'RIGHT_PAREN',
            '{': 'LEFT_BRACE',
            '}': 'LEFT_PAREN',
            ',': 'COMMA',
            '.': 'DOT',
            '-': 'MINUS',
            '+': 'PLUS',
            ';': 'SEMICOLON',
            '/': 'SLASH',
            '*': 'STAR',
            '!': 'BANG',
            '=': 'EQUAL',
            '<': 'LESS',
            '>': 'GREATER',
        }
        self.two_char_tokens = {
            '<=': 'LESS_EQUAL',
            '==': 'EQUAL_EQUAL',
            '>=': 'GREATER_EQUAL',
        }
        self.keywords = {
                "AND",
                "CLASS",
                "ELSE",
                "FALSE",
                "FUN",
                "FOR",
                "IF",
                "NIL",
                "OR",
                "PRINT",
                "RETURN",
                "SUPER",
                "THIS",
                "TRUE",
                "VAR",
                "WHILE",

                "EOF",
        }

    def scan_tokens(self):
        """
        Scans the passed file for and returns tokens
        """
        tokens = []
        with open(self.source_file) as f:
            file_content = f.read()
            line = 1
            start = 0
            current = 0
            file_content_length = len(file_content)
            it = iter(file_content)
            for n, char in enumerate(it):
                if file_content[n:n+2] == '//':
                    # handle comments
                    char = next(it)
                    while char != '\n':
                        char = next(it)
                    line += 1
                    continue
                elif char == "\n":
                    line += 1
                    continue
                elif char == " ":
                    continue
                elif char in self.single_char_tokens:
                    ttype = self.single_char_tokens[char]
                    lexeme = char
                    tokens.append(LoxToken(ttype, lexeme, "", line))
                    continue
                elif file_content[n:n+2] in self.two_char_tokens:
                    ttype = self.single_char_tokens[char]
                    lexeme = char
                    tokens.append(LoxToken(ttype, lexeme, "", line))
                    continue
                else:
                    tokens.append(f"Unknown {char}")
                    


        return tokens
