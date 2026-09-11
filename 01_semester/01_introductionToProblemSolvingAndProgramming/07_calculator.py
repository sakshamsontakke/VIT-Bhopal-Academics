# writing a program and create a calculator with function 
def calculator(a , b , choice):
    if choice == -1:
        print("exited the program")
    elif choice == 1:
        sum = a + b
        print(sum)
    elif choice == 2:
        sub = a-b
        print(sub)
    elif choice == 3:
        mul = a*b
        print(mul)
    elif choice == 4:
        div = float(a/b)
        print(div)
    else:
        print("enter valid choice")
calculator(5 , 5 , 3)