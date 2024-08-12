# A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing
# all non-alphanumeric characters,
# it reads the same forward and backward. Alphanumeric characters include letters and numbers.
# Given a string s, return true if it is a palindrome, or false otherwise.


def is_palindrome(s: str) -> bool:
    clean_string = ''.join([elem for elem in s.lower() if elem.isalnum()])
    head = 0
    tail = len(clean_string) - 1
    while head < tail:
        if clean_string[head] != clean_string[tail]:
            return False
        else:
            head += 1
            tail -= 1
    return True
