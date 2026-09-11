import calculatorModule

num1 = int(input("enter a number: "))
num2 = int(input("enter a number: "))
sum = calculatorModule.sum(num1 , num2)
sub = calculatorModule.sub(num1 , num2)

calculatorModule.myInput()

print(sum)
print(sub)