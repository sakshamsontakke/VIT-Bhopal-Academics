# 1 + 121 + 12321 + 1234321 + 123454321

n = int(input("enter a number: "))
temp  = ""
sum = 0
for i in range(1 , n+1):
    for j in range(1 , len(temp)+3):
        temp += str(i)
    sum += int(temp)  

    

