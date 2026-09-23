# write a program to concate 2 arrays without using "+" operator 

from array import*

array1 = array("i" , [1,2,3])
array2 = array("i" , [4,5,6])

n , j = len(array1) + len(array2) , 0
array3 = array("i" , [0]*n)

for i in range(n):
    if i < len(array1):
        array3[i] = array1[i]
    else:
        array3[i] = array2[j]
        j += 1    
print(array3)            