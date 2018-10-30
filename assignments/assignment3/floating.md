# IEEE foating point representation

## 1. Does any of the above three components play a role in the defining the Precession of the number ? If so which are the component or Components  which play the  role in defining precession  and how ?

Among the three components, the fractional part plays a role in defining the precision of the number. The sign bit just gives information of whether the number is positive or negative, and the exponent just gives the informtion of what exponent of 2 should be multiplied by the fractional part, to get the actual number. It is the fractional part which contains the informtion of the value that the number represents. 
For a better understanding, let us take a simple example. Even though the numbers are represented in binary, and it is the exponent of 2 by which we multiply, for the example let us consider decimal because it is more intuitive. ALso, it is the principle of precision that we have to understand, so whether it is binary or decimal, it does not matter.   
Eg: Let us look at representing the number PI. Now, consider representing it in 16 bits, 32 bits and 64 bits:    
**16 bit(approx 4 decimal places):** PI= 3.1415 . 
**32 bit(approx 7 decimal places):** PI= 3.1415926 . 
**64 bit(approx 14 decimal places):** PI= 3.14159265358979 . 
Of the three of them, the 64 bit representation is most closest to the actual value of PI. As and how we reduce the number of decimal places, the number starts getting farther from the actual value. So, it is the fractional part which defines the precision.

## 2. What is Normal and Subnormal  Values as per IEEE 754  standards  explain this  with the  help of number line

Let us take the example of half precision floating point(16 bits) to understand the normal and subnormal numbers. The format is first bit is sign bit, next 5 bits are for exponent and the rest 10 bits are for the fractional part. Implicitly there is a leading 1 assumed for the fractional part. So, now the least exponent is 2^-14 (because all zeros in exponent are not allowed). So, for numbers below 1 * 2^-14, we cannot represent them. So to increase the range, what is done is, when all zero exponent is present, then a leading one is not assumed. So, there can e as many leading zeros as wanted, and hence we can represent much more lower numbers. But, this will be at a cost of precision, because most of the fractional part will now be zeros. 


## 3. Rounding modes:

IEEE 754 provides 5 kinds of rounding modes:
1. Round to nearest even: rounds to the nearest value; if the number falls midway, it is rounded to the nearest value with an even least significant digit. Eg: 11.5 and 12.5 will both be rounded to 12.0   
2. Round to nearest, away from zero: rounds to nearest, but when in midway, rounds away from zero.  
Eg: 11.5 will be rounded to 12 and 12.5 will be rounded to 13.
3. Rounded toward zero : Similar to truncation. The last decimal place will just be removed. Eg 12.1, 12.3,..12.9 all will be rounded to 12.   
4. Rounded toward infinity: Also known as ceiling. It is just going to take the next high value. Eg: 12.1,12.2..12.9 all will be rounded to 13.  
5. Rounded toward -infinity: Also known as floor. It is going to select the preveious low value. Eg: 12.1,12.2 .. 12.9 will all be rounded to 12
