# converting a decimal to hexa decimal value 

n = int(input("enter a value: "))

number = ""

hexa = "0123456789ABCDEF"

while n > 0:

    digit = n % 16

    number = hexa[digit] + number

    n = n // 16

print(number)