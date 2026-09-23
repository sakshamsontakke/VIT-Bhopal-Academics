# 1sqr + 2sqr + 3sqr + 4sqr + ... + nsqr
n = int(input("enter a value: "))
power = 2
sum = 0
for i in range(1 , n+1):
        sum = sum + i**power
print(sum)        


