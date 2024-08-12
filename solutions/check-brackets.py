# {} - True
# [{()(())} - False
# [} - False


def all_brackets(string: str) -> bool:
    stack = []
    for elem in string:
        if elem == '(' or elem == '[' or elem == '{':
            stack.append(elem)
        elif elem == ')':
            if '(' in stack:
                stack.remove('(')
            return False
        elif elem == ']':
            if '[' in stack:
                stack.remove('[')
            return False
        elif elem == '}':
            if '{' in stack:
                stack.remove('{')
            return False
    return not stack


print(all_brackets('{}'))