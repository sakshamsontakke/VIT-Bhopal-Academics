# decimal to binary without using string function 

# zero will not be there in the output if it's in the starting of the output that is the the reason we use string to perform binary opeartions
n = 14
decimal = 0
rem = 0
while n > 0:
    rem = n%2
    decimal = decimal*10 + rem
    n = n//2
print(decimal)    