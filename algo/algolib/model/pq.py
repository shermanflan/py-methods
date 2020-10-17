from itertools import count
from heapq import heappush, heappop


# TODO:
"""
Consider re-heapify when updating a priority, instead of reinserting.
Use algolib.model.heap instead of built in.
"""


class PriorityQueueException(Exception):
    pass


class PriorityQueue:
    """
    Priority queue implementation built on top of heapq with additions
    to handle tuple comparison breaks and ties (adaptable).

    Instead of an entry_finder dictionary, the item's position in the
    heap could be stored as an index property in the item tuple.

    Based on https://docs.python.org/3/library/heapq.html.
    """
    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = count()  # unique sequence count (like IDENTITY)

    def add(self, task, priority=0):
        """
        Add a new task or update the priority of an existing task

        :param task:
        :param priority:
        :return: None
        """
        if task in self.entry_finder:
            self.__remove(task)
        unq = next(self.counter)
        entry = [priority, unq, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def __remove(self, task):
        """
        Mark an existing task as REMOVED. Raise KeyError if not found.

        :param task:
        :return: None
        """
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def remove_min(self):
        """
        Remove and return the lowest priority task. Raise KeyError if empty.

        :return: the next Task
        """
        while self.pq:
            priority, unq, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task

        raise KeyError('pop from an empty priority queue')

    def min(self):
        """
        Peek but do not remove min.
        """
        raise NotImplementedError()

    def __repr__(self):
        return str(self.pq)

    def __len__(self):
        return len(self.entry_finder)

    def __contains__(self, item):
        return item in self.entry_finder
