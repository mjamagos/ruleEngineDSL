
class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(f"{name} is not defined")

    def assign(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise NameError(f"{name} is not defined")


class Literal:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name


class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Block:
    def __init__(self, statements):
        self.statements = statements


class If:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Declare:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print:
    def __init__(self, value):
        self.value = value


class Evaluator:
    def __init__(self):
        self.environment = Environment()

    def evaluate(self, node):
        if isinstance(node, Literal):
            return node.value

        elif isinstance(node, Variable):
            return self.environment.get(node.name)

        elif isinstance(node, Binary):
            left = self.evaluate(node.left)

            if node.operator == "and":
                if not isinstance(left, bool):
                    raise TypeError("Condition must be True or False")

                if not left:
                    return False

                right = self.evaluate(node.right)

                if not isinstance(right, bool):
                    raise TypeError("Condition must be True or False")

                return right

            elif node.operator == "or":
                if not isinstance(left, bool):
                    raise TypeError("Condition must be True or False")

                if left:
                    return True

                right = self.evaluate(node.right)

                if not isinstance(right, bool):
                    raise TypeError("Condition must be True or False")

                return right

            right = self.evaluate(node.right)

            if node.operator == "+":
                return left + right
            elif node.operator == "-":
                return left - right
            elif node.operator == "*":
                return left * right
            elif node.operator == "/":
                return left / right
            elif node.operator == "%":
                return left % right
            elif node.operator == "==":
                return left == right
            elif node.operator == "!=":
                return left != right
            elif node.operator == ">":
                return left > right
            elif node.operator == "<":
                return left < right
            elif node.operator == ">=":
                return left >= right
            elif node.operator == "<=":
                return left <= right
            else:
                raise ValueError(f"Unknown operator: {node.operator}")

        elif isinstance(node, Declare):
            value = self.evaluate(node.value)
            self.environment.define(node.name, value)
            return value

        elif isinstance(node, Assign):
            value = self.evaluate(node.value)
            self.environment.assign(node.name, value)
            return value

        elif isinstance(node, Print):
            print(self.evaluate(node.value))

        elif isinstance(node, Block):
            old_environment = self.environment
            self.environment = Environment(old_environment)

            try:
                for statement in node.statements:
                    self.evaluate(statement)
            finally:
                self.environment = old_environment

        elif isinstance(node, If):
            condition = self.evaluate(node.condition)

            if not isinstance(condition, bool):
                raise TypeError("If condition must be True or False")

            if condition:
                return self.evaluate(node.then_branch)
            elif node.else_branch is not None:
                return self.evaluate(node.else_branch)

        elif isinstance(node, While):
            while True:
                condition = self.evaluate(node.condition)

                if not isinstance(condition, bool):
                    raise TypeError("While condition must be True or False")

                if not condition:
                    break

                self.evaluate(node.body)

        else:
            raise TypeError(f"Unknown node: {type(node).__name__}")


def main():
    evaluator = Evaluator()

    program = Block([
        Declare("days_left", Literal(2)),
        Declare("tasks_done", Literal(0)),

        If(
            Binary(Variable("days_left"), "<=", Literal(3)),
            Print(Literal("Deadline is near!")),
            Print(Literal("There is still time."))
        ),

        While(
            Binary(Variable("tasks_done"), "<", Literal(3)),
            Block([
                Print(Literal("Working on a task...")),
                Assign(
                    "tasks_done",
                    Binary(
                        Variable("tasks_done"),
                        "+",
                        Literal(1)
                    )
                )
            ])
        ),

        If(
            Binary(Variable("days_left"), "<", Literal(1)),
            Print(Literal("Deadline has passed!")),
            Print(Literal("Deadline has not passed yet."))
        )
    ])

    evaluator.evaluate(program)


if __name__ == "__main__":
    main()