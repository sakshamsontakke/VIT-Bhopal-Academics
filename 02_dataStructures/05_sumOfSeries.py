# 1 + 1/2! + 1/3! + ... + 1/n!

n = int(input("Enter a value: ")) 
total_sum = 0
val = 1 
for i in range(1, n + 1):
    val *= i             
    total_sum += 1 / val

print("The sum of the series is:", total_sum)
