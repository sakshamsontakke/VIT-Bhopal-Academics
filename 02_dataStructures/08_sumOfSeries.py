# 1 + 1/3 + 1/5 + 1/7 + .....+ 1/2power(n-1)
n = int(input("enter a value: "))
sum = 0
for i in range(1 , n+1 , 2):
    sum += 1/i
print(sum)    