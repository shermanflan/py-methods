class StackError(Exception):
    """Base class for exceptions in this module."""
    pass


# Opt1: Use an array as the model container.
class Stack(object):
    """
    Uses a list as a stack. Pop/Append natively create
    a stack model structure. Canonical implementation uses
    a linked list as a base model structure.
    """
    def __init__(self, *args):
        super().__init__()
        self.__values = list(args)
        self.__size = len(args)

    def pop(self):
        if self.__values:
            self.__size -= 1
            return self.__values.pop()
        else:
            raise StackError(f'pop({self.__values}): Stack is empty!')

    def push(self, data):
        self.__size += 1
        self.__values.append(data)

    def peek(self):
        if self.__values:
            return self.__values[-1] # peek at top of stack
        else:
            raise StackError('peek(): Stack is empty!')

    def is_empty(self):
        if self.__values:
            return True
        else:
            return False

    def size(self):
        return self.__size

    # Implement __repr__ for any class you implement. This should be second nature.
    # Implement __str__ if you think it would be useful to have a string version
    # which errs on the side of more readability in favor of more ambiguity.
    def __repr__(self):

        return str(self.__values)