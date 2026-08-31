# write a program to find the fibonacci series till n terms
n = int(input("enter a number"))
a = 0
b = 1
c = a + b
i = 0
print(a)
print(b)
while i < n:
    print(c)
    a = b
    b = c
    c = a + b
    i += 1


    

