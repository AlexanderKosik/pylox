from loxtoken import LoxToken
import re

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
            '}': 'RIGHT_BRACE',
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
            '!=': 'BANG_EQUAL',
            '>=': 'GREATER_EQUAL',
        }
        self.keywords = {
                'and': 'AND',
                'class': 'CLASS',
                'else': 'ELSE',
                'false': 'FALSE',
                'fun': 'FUN',
                'for': 'FOR',
                'if': 'IF',
                'nil': 'NIL',
                'or': 'OR',
                'print': 'PRINT',
                'return': 'RETURN',
                'super': 'SUPER',
                'this': 'THIS',
                'true': 'TRUE',
                'var': 'VAR',
                'while': 'WHILE',

                'eof': 'EOF',
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

            # scanning numbers
            if self.content[n].isdigit():
                start = n
                try:
                    while self.content[n].isdigit():
                        n += 1
                except IndexError as e:
                    # we have reached EOF
                    pass

                value = self.content[start:n]
                token_type = 'NUMBER'
                tokens.append(LoxToken(token_type, value, '', line))
                continue

            # scanning strings
            if self.content[n] == '"':
                start = n
                n += 1
                try:
                    while self.content[n] != '"':
                        n += 1
                except IndexError as e:
                    # we have reached EOF
                    print('Error. Unterminated string.')
                    break
                value = self.content[start+1:n]
                token_type = 'STRING'
                tokens.append(LoxToken(token_type, value, '', line))
                n += 1
                line += 1
                continue


            if self.content[n:n+2] in self.two_char_tokens:
                lexeme = self.content[n:n+2]
                token_type = self.two_char_tokens[lexeme]
                tokens.append(LoxToken(token_type, lexeme, '', line))
                # move forward two times because of 2 char operator
                n += 2
                continue

            if self.content[n] in self.single_char_tokens:
                token_type = self.single_char_tokens[self.content[n]]
                lexeme = self.content[n]
                tokens.append(LoxToken(token_type, lexeme, '', line))
                n += 1
                continue


            if self.content[n].isidentifier():
                start = n
                reg_exp = r'[a-zA-Z_]+'
                match = re.match(reg_exp, self.content[n:])
                if match:
                    identifier = match.group(0)
                    token_type = self.keywords.get(identifier, 'IDENTIFIER')
                    tokens.append(LoxToken(token_type, identifier, '', line))
                    n += len(identifier)
                else:
                    print(f'Invalid character in identifier')
                    n += 1
                continue

                    
            print(f'Unknown lexeme {self.content[n]}')
            n += 1


        tokens.append(LoxToken('EOF', '', '', line))
                

        return tokens
