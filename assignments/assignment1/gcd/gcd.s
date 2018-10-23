	;Krishna Nagaraja
	; IMT2015512
	THUMB    
	AREA     appcode, CODE, READONLY
	EXPORT __main
	ENTRY 
__main  FUNCTION	; program to find greatest of three numbers	 		
		MOV  r0, #0x6; first number
		MOV  r1, #0x1 ; second number
		 
loop	CMP r0,r1
		SUBGT r0,r0,r1
		SUBLT r1,r1,r0
		BNE loop
		MOV r3,r1; r3 will store the gcd
stop 	B stop
		ENDFUNC
		END

; Testing
; input r0=0x6,r1=0x1, output r3=0x1
; input r0=0x6,r1=0x12, output r3=0x6
; input r0=0x2,r1=0x1, output r3=0x1
; input r0=0x2,r1=0x3, output r3=0x1
