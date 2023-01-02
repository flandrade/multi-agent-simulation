def normalize(value, min, max):
    if value < min:
        return min
    elif value > max - 1:
        return max
    else:
        return value
