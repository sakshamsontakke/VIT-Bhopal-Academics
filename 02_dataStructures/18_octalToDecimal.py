# converting octal to decimal 

octal = input("enter a binary number : ")
n = len(octal) - 1
decimal = 0
for i in octal:
    decimal += int(i)*(2**n)
    n = n-1

print(decimal)    

