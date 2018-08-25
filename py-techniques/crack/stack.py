class StackError(Exception):
    """Base class for exceptions in this module."""
    pass

class stack(object):
    """
    Uses a list as a stack. Pop/Append natively create
    a stack data structure. Canonical implementation uses
    a linked list as a base data structure.
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
            return self.__values[0]
        else:
            raise StackError('peek(): Stack is empty!')

    def isEmpty(self):
        if self.__values:
            return True
        else:
            return False

    def size(self):
        return self.__size

    def __repr__(self):

        return str(self.__values)