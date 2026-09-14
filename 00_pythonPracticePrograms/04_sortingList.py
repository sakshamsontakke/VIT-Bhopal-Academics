# write a program to sort a list without using any predefined functions

l = [7, 3, 5, 9, 1, 2, 4, 8, 2, 6]

i = 0

while i < len(l):
    j = 0

    while j < len(l) - 1:
        if l[j] > l[j + 1]:
            l[j], l[j + 1] = l[j + 1], l[j]

        j += 1

    i += 1

print(l)