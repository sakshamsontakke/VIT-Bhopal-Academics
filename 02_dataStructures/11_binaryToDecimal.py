# write a program to covert binary into decimal value 

binaryNum = input("enter a binary number : ")
n = len(binaryNum) - 1
decimal = 0
for i in binaryNum:
    decimal += int(i)*(2**n)
    n = n-1

print(decimal)    

