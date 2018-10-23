	;Krishna Nagaraja
	; IMT2015512
	THUMB    
	AREA     appcode, CODE, READONLY
	EXPORT __main
	ENTRY 
__main  FUNCTION	; Program to find ith element in fibonacci series	 		
		 MOV  r0, #0x2; the value of i (so #0x02 would mean we want to find 2nd element)
		 MOV  r1, #0x0 ; The first element in fibonacci series
		 MOV  r2, #0x1 ; The second element in fibonacci series
         
		 CMP r0,#2
		 MOVLT r3,r1 ; if less than, it means input =1, we want first element which is 0
		 MOVEQ r3,r2 ; if equal to, it means input=2, we want second element which is 1
		 SUBGT r0,r0,#2 ; if greater, then we subtract by 2 before we enter loop
		 BLT stop ; if it was lesser then we already have the output, so stop
		 BEQ stop ; if it was equal , then we already have the output, so stop
		 
loop	 ADD r4,r1,r2
		 MOV r1,r2
		 MOV r2,r4
		 SUBS r0,r0,#1
		 BNE loop
		 MOV r3,r4  ; output available in r3 at the end
stop 	 B stop
		 ENDFUNC
		 END

;Testing
; r0=0x1 , output r3=0
; r0=0x2 , output r3=1
; r0=0x3 , output r3=1
; r0=0x5 , output r3=3


