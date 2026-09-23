# 1 + 12 + 123 + 1234

n = int(input("enter a value : "))
temp = ""
sum = 0
for i in range(1 , n+1):
    temp += str(i)
    sum  += int(temp)
print(sum)    