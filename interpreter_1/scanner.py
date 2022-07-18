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
        n = 0
        while n < len(self.content):
            if self.content[n:n+2] == '//':
                # handle comments
                try:
                    while self.content[n] != '\n':
                        n += 1
                except IndexError as e:
                    # we have reached EOF
                    break
                line += 1
                continue

            if self.content[n] == '\n':
                line += 1
                n += 1
                continue

            if self.content[n].isspace():
                n += 1
                continue

            if self.content[n:n+2] in self.two_char_tokens:
                lexeme = self.content[n:n+2]
                token_type = self.two_char_tokens[lexeme]
                tokens.append(LoxToken(token_type, lexeme, '', line))
                # move forward one more time because of 2 char operator
                n += 2
                continue

            if self.content[n] in self.single_char_tokens:
                token_type = self.single_char_tokens[self.content[n]]
                lexeme = self.content[n]
                tokens.append(LoxToken(token_type, lexeme, '', line))
                n += 1
                continue
            else:
                tokens.append(f'Unknown {self.content[n]}')

        tokens.append(LoxToken('EOF', '', '', line))
                

        return tokens
