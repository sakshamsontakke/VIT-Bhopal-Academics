# 1 + 121 + 12321 + 1234321 + 123454321

n = int(input("Enter n: "))

number = 0
total = 0

for i in range(1, n + 1):
    number = number * 10 + i
    total = total + number * number

print("Sum =", total)