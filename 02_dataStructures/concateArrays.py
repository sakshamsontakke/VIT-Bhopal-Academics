# write a program to concate 2 arrays without using "+" operator 

from array import*

array1 = array("i" , [1,2,3])
array2 = array("i" , [4,5,6])
array3 = array("i" , [])

n , j = len(array1) + len(array2) , 0

for i in range(n):
    if i < len(array1):
        array3.append(array1[i])
    else:
        array3.append(array2[j])
        j += 1    
print(array3)            