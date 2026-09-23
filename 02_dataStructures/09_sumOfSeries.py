# student wants to calculate total electricity bill using a series where charge of each succesive unit 
# increase by 2 rupees , write a program to calculate total charge for n units
n = int(input("enter a value: "))
bill = 0
charge = 2
for i in range(n):
        bill = bill + charge
        charge = charge + 2
print(bill)        
