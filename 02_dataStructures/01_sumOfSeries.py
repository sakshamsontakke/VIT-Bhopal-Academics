#  1 + 2 + 3 + ... + n

n = int(input("enter a number: "))
for i in range(1 , n + 1):
    if(i == n):
        print(i , end= " ")
    else:
        print(i ,end=" + ")