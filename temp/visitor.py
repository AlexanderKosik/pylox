class Bike:
    def __init__(self):
        self.speed = 0

    def accept(self, visitor):
        visitor.visit(self)

class EBike:
    def __init__(self):
        self.speed = 0

    def accept(self, visitor):
        visitor.visit(self)


class Accelerate:
    def visit(self, visitee):
        if isinstance(visitee, Bike):
            visitee.speed += 5
        elif isinstance(visitee, EBike):
            visitee.speed += 10


