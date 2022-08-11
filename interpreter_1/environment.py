from loxtoken import LoxToken

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: LoxToken, value):
        self.values[name.lexeme] = value

    def get(name: LoxToken):
        try:
            return self.values[name.lexeme]
        except KeyError:
            raise Exception("Undefined variable '{name.lexeme}')
