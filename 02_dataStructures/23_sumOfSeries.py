# 1 + 121 + 12321 + 1234321 + 123454321

n = int(input("enter a number: "))
term = ""
sum = 0
for i in range(1 , n+1):
    term = str(1)*i
    sum = int(term)**2
    print(term , sum)
print(sum)