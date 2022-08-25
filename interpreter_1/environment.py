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
