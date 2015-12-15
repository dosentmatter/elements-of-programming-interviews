import random

def randlist_duplicates(max_number, length, min_number=0):
    return \
    [random.randint(min_number, max_number) for _ in range(length)]

def randlist_no_duplicates(max_number, length, min_number=0):
    return random.sample(range(min_number, max_number + 1), length)
