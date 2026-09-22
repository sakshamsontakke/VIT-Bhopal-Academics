# converting decimal to binary number using string
n = int(input("enter a value: "))
binary = ""
while n>0:
    binary += str(n%2)
    n = n // 2

print(binary)