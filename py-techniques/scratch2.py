from collections import deque

class queue(object):
    def __init__(self):
        super().__init__()
        self.data = deque()

    def enqueue(self, data):
        self.data.append(data)

    def dequeue(self):
        return self.data.popleft()

    def peek(self):
        return self.data[0]

    def __str__(self):
        return self.data.__str__()

def main():
    s1 = queue()
    s1.enqueue(1)
    s1.enqueue('2')
    s1.enqueue(3)
    print(s1)
    print(s1.peek())
    print(s1.dequeue())
    print(s1.dequeue())
    print(s1.dequeue())

    print(s1)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()