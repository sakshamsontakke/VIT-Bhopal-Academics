# finding prime number or not 

n = int(input("enter a number: "))
count = 0
i = 1
while i <= n:
    if n%i == 0:
        count += 1
    i += 1
if count > 2:
    print(f"the given number {n} is not a prime number")
else:
    print(f"the given number {n} is prime number")            