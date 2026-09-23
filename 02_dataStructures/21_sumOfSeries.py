# 1 + 22 + 333 + 4444 + 55555 + ....

n = int(input("enter a value : "))
temp = ""
sum = 0
for i in range(1 , n+1):
    temp = str(i)*i
    current += 1
    sum += int(temp)
print(sum)    
