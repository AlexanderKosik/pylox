from loxtoken import LoxToken

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value):
        self.values[name] = value

    def get(self, name: str):
        # first try the 'local scope'
        if name in self.values:
            return self.values[name]

        # check surrounding scopes recursivly
        if self.enclosing is not None:
            return enclosing.get(name)
        
        raise Exception("Undefined variable '{name}'")

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise Exception(f"Undefined variable '{name}'.")
