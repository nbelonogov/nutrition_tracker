# You are given a nested list of integers nestedList.
# Each element is either an integer or a list whose elements may also be integers or other lists. Implement an iterator to flatten it.


def unpacking(nestedlist):
    res = []
    for elem in nestedlist:
        if isinstance(elem, int):
            res.append(elem)
        else:
            res += unpacking(elem)
    return res
