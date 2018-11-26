 ;Gogigeni Dharmik
  ;Krishna Nagaraja
  ;Bhaskara Viswesh
  area appcode, CODE, READONLY
  export __main
  ENTRY
__main function
	;R2 stores the Origin
	;R1 has the address of the stack where the coordinate list starts
	LDR R2,=0x22223000;ASSUMING R2 STORES (X,Y) AS FIRST HALF WORD IS X AND NEXT HALF IS Y
	LDR R4,=0xFFFF0000; Throughout the code, the format of (x,y) is first halfword is x and second halfword is y
	AND R5,R2,R4;r5 HAS X:(X,0)
	SUB R6,R2,R5;R6 HAS Y:(0,Y)
	LSR R5,R5,#16;
	MOV R7,#0;
	LDR R1,=0X20000000;STARTING ADDRESS
	MOV R8,#240;
	
LOOP1 STRH R7,[R1,#0];
	  STRH R6,[R1,#2];
	  ADD R7,R7,#1;
	  ADD R1,R1,#4;
	  CMP R7,R8;
	  BNE LOOP1;
	  MOV R7,#0;
      MOV R8,#320;
LOOP2 STRH R5,[R1,#0];
	  STRH R7,[R1,#2];
	  ADD R7,R7,#1;
	  ADD R1,R1,#4;
	  CMP R7,R8;
	  BNE LOOP2;
	  
stop B stop ; stop program
	endfunc
	end