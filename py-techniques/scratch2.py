import math
from collections import deque



if __name__ == '__main__':
    suits = ['H', 'S', 'C', 'D']
    card_val = (list(range(1, 11)) + [10] * 3) * 4

    print(card_val)
    base_names = ['A'] + list(range(2, 11)) + ['J', 'K', 'Q']

    print(base_names)
    cards = []
    for suit in ['H', 'S', 'C', 'D']:
        cards.extend(str(num) + suit for num in base_names)

    print(cards)
