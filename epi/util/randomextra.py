import random

def randlist(max_number, length, min_number=0):
    return \
    [random.randint(min_number, max_number) for _ in range(length)]
