# 1 + 1/2 + 1/3 + ......+ 1/n
n = int(input("enter a value: "))
sum = 0
for i in range(1  , n + 1):
    sum += 1/i
print(sum)    