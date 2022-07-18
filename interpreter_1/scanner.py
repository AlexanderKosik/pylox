from loxtoken import LoxToken

class Scanner:
    @staticmethod
    def from_file(file_name):
        with open(file_name) as f:
            content = f.read()
            return Scanner(content)
        return None

    def __init__(self, content):
        self.content = content
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
                'AND',
                'CLASS',
                'ELSE',
                'FALSE',
                'FUN',
                'FOR',
                'IF',
                'NIL',
                'OR',
                'PRINT',
                'RETURN',
                'SUPER',
                'THIS',
                'TRUE',
                'VAR',
                'WHILE',

                'EOF',
        }

    def scan_tokens(self):
        '''
        Scans the passed file for and returns tokens
        '''
        tokens = []
        line = 1
        start = 0
        current = 0
        file_content_length = len(self.content)
        it = iter(self.content)
        n = 0
        for char in it:
            if self.content[n:n+2] == '//':
                # handle comments
                while char != '\n':
                    try:
                        char = next(it)
                    except StopIteration as e:
                        # we have reached EOF
                        break
                line += 1
                n += 1
                continue
            elif char == '\n':
                line += 1
                n += 1
                continue
            elif char == ' ':
                n += 1
                continue
            elif self.content[n:n+2] in self.two_char_tokens:
                lexeme = self.content[n:n+2]
                token_type = self.two_char_tokens[lexeme]
                tokens.append(LoxToken(token_type, lexeme, '', line))
                # move forward one more time because of 2 char operator
                next(it)
                n += 2
                continue
            elif char in self.single_char_tokens:
                token_type = self.single_char_tokens[char]
                lexeme = char
                tokens.append(LoxToken(token_type, lexeme, '', line))
                n += 1
                continue
            else:
                tokens.append(f'Unknown {char}')

        tokens.append(LoxToken('EOF', '', '', line))
                

        return tokens
