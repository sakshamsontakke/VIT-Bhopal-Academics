# 1 +2sqr + 3sqr .... 
n = int(input("eneter a value: "))
sum = 0 
for i in range(1 , n+1):
    sum += i**i
print(sum)    