from collections import defaultdict

class node(object):
    """Singly linked"""
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.next = None

    def __str__(self): # like ToString
        return str(self.data)

# Opt1: Adding and maintaining self.tail would make append more efficient.
# Opt2: Adding and maintaining self.count would make size() more efficient.
# Opt3: Add an enumerator using yied in a while loop.
# Opt4: Create a doubly linked list class.
class linkedlist(object):
    """Wrapper for node"""
    def __init__(self, data):
        self.head = node(data)

    def insert(self, data):
        newHead = node(data)
        newHead.next = self.head
        self.head = newHead

    def append(self, data):
        end = node(data)
        tmp = self.head

        while tmp.next != None:
            tmp = tmp.next

        tmp.next = end
        return tmp.next
    
    def appendNode(self, data):
        tmp = self.head

        while tmp.next != None:
            tmp = tmp.next

        tmp.next = data
        return tmp.next

    # Opt1: Adding and tracking a prev variable simplifies logic
    def delete(self, data):
        if self.head.data == data:
            self.head = self.head.next

        tmp = self.head

        while tmp.next != None:
            if tmp.next.data == data:
                tmp.next = tmp.next.next
                break

            tmp = tmp.next
    
    @staticmethod
    def findMiddle(node):
        """ In one pass """
        start = node
        startplus2 = node

        while startplus2 and startplus2.next:
            start = start.next
            startplus2 = startplus2.next.next

        return start

    def isCycle(self):
        turtle = self.head
        hare = self.head

        while hare and hare.next:
            turtle = turtle.next
            hare = hare.next.next

            if turtle == hare:
                return True

        return False

    @staticmethod
    def reverse(node):
        """ In one pass, no stack 
            See: https://www.geeksforgeeks.org/reverse-a-linked-list/
        """

        prevnode, currnode, nextnode = None, node, None

        while currnode:
            # Save next
            nextnode = currnode.next

            # Point to previous (initially None)
            currnode.next = prevnode 

            # Move forward
            prevnode = currnode
            currnode = nextnode

        return prevnode

    @staticmethod
    def dedup(node):
        """ In one pass, sorted or unsorted """        
        prevnode, currnode = None, node
        dups = defaultdict(int)

        while currnode:
            if currnode.val in dups: # seen before
                prevnode.next = currnode.next # delete
            else:
                dups[currnode.val] += 1
                prevnode = currnode # will be initialize here

            currnode = prevnode.next
        return node

    def __str__(self): # like ToString
        tmp = self.head
        s = ''

        if self.isCycle():
            return 'Cycle detected!'

        while tmp != None:
            s += str(tmp) + ' => '
            tmp = tmp.next

        return s + 'Null'