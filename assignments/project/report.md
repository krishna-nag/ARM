# Compiler

## Python


## Data types
- integer
- float
- boolean

</br>

## Declarations

```python
integer = 2

float = 3.4

bool = True

# No Arrays
# No string
```

## Operators

### Arithmetic
|Operator|Description|
|--------|-----------|
|`+`|addition|
|`-`|subtraction|
|`*`|multiplication|
|`/`|quotient|
|`%`|remainder|

### Comparison
|Operator|Description|
|--------|-----------|
|`==`|equal|
|`!=`|not equal|
|`<`|less than|
|`<=`|less than or equal|
|`>`|greater than|
|`>=`|greater than or equal|

<!-- ### Logical
|Operator|Description|
|--------|-----------|
|`and`|logical and|
|`or`|logical or|
|`not` or `!`|logical not| -->

<!-- ### Other
|Operator|Description|
|--------|-----------|
|`in`|Returns true if an element is in array|
|`..`|List expansion| -->



## if-else

```python
if condition1:
   ...
elif condition2:
   ...
else:
   ...

// Example:
if 3 in [1, 2, 3]:
  println "Exists"

# Array and strings are not
# implemented, btw

```




## Functions
```python
# Incomplete implementation
```


# Compiler Implementation
- First the python file is converted into an Abstract Syntax Tree, using python's ast module.
- This astree is recursively broken down using two functions: 
  - Compile: Looks at the code and tries to generate the assembly code
  - evaluate: If there is an expression (binary operation,boolean operation, comparison), then that expression is given to the evaluate function to recursively evaluate it and generate the assembly code.
- This style of compilation is inspired from LISP programming language.
- Memory usage: So, this compiler uses 32Kb of program memory, 4kb of temporary memory, and all registers and float single precision registers
  -0x20000000 to 0x20007FFF is program memory where variables are allocated
  -0xE0000000 to 0xE0000FFF is 4kb temporary memory, used for internal operations. These memory locations are allocated and freed from time to time.
  -Similarly all registers are allocated and freed from time to time

## Int and float compatibility
- This compiler is able to achieve compatibility between these types
- It means that any operation can be performed on these types without explicitly converting them
- Ex:
```python
x = 10.1
y = 1
z = x+y #This works even if x and y are of different types
```
- Similarly all arithmetic and logical operations can be performed on these types without any problem.

# Input and Output
- The Input would be a .py file, which would contain the python code you would want to compile
```bash
python start.py > assembly_file_name.s
Enter file name :<enter your file name here>
```
- Then the output would appear in the assembly_file_name.s file which you can directly use in keil to assemble it.

### Sample Input:
```python
x = 10.11
y = 90
y = x*y
```

### Output:
```arm
  area appcode, CODE, READONLY
  export __main
  ENTRY
__main function



    VLDR.F32 S9,=10.11
    VMOV.F R4, S9
    LDR R5,=3758098432
    STR R4, [R5]
    LDR R4,= 536870912
    LDR R5,= 3758098432
    LDR R6, [R5]
    STR R6, [R4]


    LDR R4,=90
    LDR R5,=3758098432
    STR R4, [R5]
    LDR R4,= 536870916
    LDR R5,= 3758098432
    LDR R6, [R5]
    STR R6, [R4]


    LDR R4,=536870912
    VLDR.F32 S9 ,[R4]
    LDR R5,=536870916
    LDR R4,[R5]
    VMOV.F32 S8,R4
    VCVT.F32.S32 S8, S8
    VMUL.F S8,S8,S9
    VMOV.F32 R4, S8
    LDR R5, =3758098432
    STR R4, [R5]
    LDR R4,= 536870916
    LDR R5,= 3758098432
    LDR R6, [R5]
    STR R6, [R4]
END
```
