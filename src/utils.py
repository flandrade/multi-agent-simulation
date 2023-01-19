import random

def decision(probability):
    return random.random() <= probability

def normalize(value, min, max):
    if value < min:
        return min
    elif value > max - 1:
        return max
    else:
        return value
