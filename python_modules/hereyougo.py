# my python version
def f(c):
    if c == 1: return str(c) + '0' + str(c)
    return str(c) + f(c-2) + str(c)
