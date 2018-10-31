class LLNode(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.next = None

    def __str__(self):
        return self.name

A = LLNode('one')
B = LLNode('two')
C = LLNode('three')
D = LLNode('four')
E = LLNode('five')

A.next = B
B.next = C
C.next = D
D.next = E

def kth_to_last_node(k, n):
    step = 0

    # Go k steps forward
    head = n
    while head and step < k-1:
        #print(head)
        head = head.next
        step += 1

    #print('======={0}'.format(head))
    if step < k-1:
        raise Exception('Invalid k')

    # Increment head and kth until end of list
    kth = n
    while head.next:
        #print(head, kth)
        kth = kth.next
        head = head.next

    return kth

print(kth_to_last_node(2, A))