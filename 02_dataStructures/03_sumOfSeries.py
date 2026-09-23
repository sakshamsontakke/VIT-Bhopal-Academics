# 2 + 4 + 6 + 8 ..

n = int(input("enter a value: "))
sum  = 0
for i in range(2 , n+1 , 2):
    sum += i
print(sum)