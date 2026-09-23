from array import *

arr = array("i", [1, 2, 3, 2, 4, 1, 5, 3])
new_arr = array("i", [0] * 10)

n = 8
m = 0

for i in range(n):
    found = 0

    for j in range(m):
        if arr[i] == new_arr[j]:
            found = 1
            break

    if found == 0:
        new_arr[m] = arr[i]
        m = m + 1

print("Array after removing duplicates:")

for i in range(m):
    print(new_arr[i], end=" ")