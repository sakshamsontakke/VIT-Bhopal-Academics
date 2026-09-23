# factorial change 

n = int(input("enter  a value: "))
sum = 0
fact = 1
for i in range( 1 , n+1):
    fact *= i
    sum += fact
print(sum)    