# IEEE foating point representation

## 1. Does any of the above three components play a role in the defining the Precession of the number ? If so which are the component or Components  which play the  role in defining precession  and how ?

Among the three components, the fractional part plays a role in defining the precision of the number. The sign bit just gives information of whether the number is positive or negative, and the exponent just gives the informtion of what exponent of 2 should be multiplied by the fractional part, to get the actual number. It is the fractional part which contains the informtion of the value that the number represents. 
For a better understanding, let us take a simple example. Even though the numbers are represented in binary, and it is the exponent of 2 by which we multiply, for the example let us consider decimal because it is more intuitive. ALso, it is the principle of precision that we have to understand, so whether it is binary or decimal, it does not matter.
Eg: Let us look at representing the number PI. Now, consider representing it in 16 bits, 32 bits and 64 bits:
**16 bit(approx 4 decimal places):** PI= 3.1415  
**32 bit(approx 7 decimal places):** PI= 3.1415926  
**64 bit(approx 14 decimal places):** PI= 3.14159265358979
Of the three of them, the 64 bit representation is most closest to the actual value of PI. As and how we reduce the number of decimal places, the number starts getting farther from the actual value. So, it is the fractional part which defines the precision.

## 2. What is Normal and Subnormal  Values as per IEEE 754  standards  explain this  with the  help of number line

Let us take the example of half precision floating point(16 bits) to understand the normal and subnormal numbers. The format is first bit is sign bit, next 5 bits are for exponent and the rest 10 bits are for the fractional part. Implicitly there is a leading 1 assumed for the fractional part. So, now the least exponent is 2^-15
