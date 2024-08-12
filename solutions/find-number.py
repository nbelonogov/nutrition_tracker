# Вычислить если такие два числа в упорядоченном списке, сумма которых равна числу (number)
# func([1,2,3,4,5], 6) --> True, тк сумма 2 и 4
# func([1,2,3,4,5], 10) --> False, тк нет таких чисел

def find_number(arr: list, number: int) -> bool:
    for i in range(len(arr)):
        if (number - arr[i]) in arr[i+1:]:
            return True
        else:
            continue
    return False