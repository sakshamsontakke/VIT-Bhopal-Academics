# write a program to convert hexa to decimal 

hexa = input("Enter hexadecimal number: ")

digits = "0123456789ABCDEF"

decimal = 0
power = 0

for i in range(len(hexa) - 1, -1, -1):

    digit = digits.index(hexa[i])

    decimal = decimal + digit * (16 ** power)

    power = power + 1

print(decimal)