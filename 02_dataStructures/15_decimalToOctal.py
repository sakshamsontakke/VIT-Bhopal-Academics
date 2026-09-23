# coverting decimal to octal using string function 

n = int(input("enter the number: "))
octal = ""
while n>0:
    octal = str(n%8)  + octal
    n = n//8
print(octal)    
