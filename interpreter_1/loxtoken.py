from dataclasses import dataclass

@dataclass
class LoxToken:
    type: str
    lexeme: str
    literal: str
    line: int

    def __repr__(self):
        return self.lexeme

