from loxtoken import LoxToken

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value):
        self.values[name] = value

    def get(self, name: str):
        try:
            return self.values[name]
        except KeyError:
            raise Exception("Undefined variable '{name}'")
