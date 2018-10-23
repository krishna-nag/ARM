	THUMB    
	AREA     appcode, CODE, READONLY
	EXPORT __main
	ENTRY 
__main  FUNCTION	; program to find greatest of three numbers	 		
		MOV  r0, #0x2; first number
		MOV  r1, #0x0 ; second number
		MOV  r2, #0x1 ; third number
         
		CMP r0,r1
		MOVGT r3,r0
		MOVLT r3,r1
		 
		CMP r3,r2
		MOVLT r3,r2; greatest of three numbers will be available in r3
		B stop
		 
stop 	 B stop
		 ENDFUNC
		 END