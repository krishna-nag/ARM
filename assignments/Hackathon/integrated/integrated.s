;Krishna Nagaraja
;Gogigeni Dharmik
; Bhaskara Viswesh
	THUMB
	AREA 	appcode, CODE, READONLY
	IMPORT printMsg             
	export __main
	ENTRY
	; Registers=>
	; R11 stores the adress from where input starts
	; R11 + 30 is the address from where encrypted output starts
	; R8 stores address from where the encoded output starts
	; R8 + 80 (0x200000B0) is address from where decoded output starts
	; R8 + 120 is adress from where decrypted output starts
	; R11 + 21 stores the key of encryption which is xor'd
	; R12 stores no of input pixels

	;So, Input starts from address at R11 => 0x20000000
	;Output starts from address R8+120 => 0x200000D8
	
	;At the end, the print section, prints a 1 if the input pixel=output pixel, 0 otherwise
	;Here number of pixels taken is 10, altering it is not allowed, since the memory could overlap
	
	

__main    FUNCTION
	  LDR R2,=0x20000000 ; Input address
	  MOV R11,R2
	  LDR R8,=0x20000060 ; 
	  MOV R2,R11
	  MOV R12,#10;
	  MOV R10,#1
	  ;Loading inputs to memory
	  STRH R10,[R2]
	  MOV R10,#2
	  STRH R10,[R2,#2]
	  MOV R10,#3
	  STRH R10,[R2,#4]
	  MOV R10,#4
	  STRH R10,[R2,#6]
	  MOV R10,#5
	  STRH R10,[R2,#8]
	  MOV R10,#6
	  STRH R10,[R2,#10]
	  MOV R10,#7
	  STRH R10,[R2,#12]
	  MOV R10,#8
	  STRH R10,[R2,#14]
	  MOV R10,#9
	  STRH R10,[R2,#16]
	  MOV R10,#10
	  STRH R10,[R2,#18]
	  MOV R6,#0;
	  MOV R9,#2;
	  
	  LDR R10,=0x77 ;setting the key
	  
	  MOV R7,#0;
	  ADD R3,R11,#21
	  STR R10,[R3]
	  ;LDR R10,[R3]
	  MOV R2,R11;
	  
Encrypt CMP R12,R6     ;Encryption => Xor with the key
		ADDEQ R11,R11,#30
		MULEQ R12,R12,R9;
		MOVEQ R6,#0
		MOVEQ R7,#0
		BEQ ENCODE
		MUL R7,R6,R9;
		LDRH R4,[R2,R7]
		EOR R4,R10
		MOV R10,R4
		ADD R3,R7,#30
		STRH R4,[R2,R3]
		ADD R6,R6,#1
		B Encrypt
	  
ENCODE CMP R12,R6    ; => (12,8) hamming code => check bits at positions 1,2,4 and 8 
	   MOVEQ R4,#0	 ; Sample input to this section: 10001100
	   MOVEQ R7,#0	 ; Sample Output of this section: 100011101001
	   MOVEQ R3,#2
	   MOVEQ R1,R12
	   BEQ DECODE
	  LDRH R1,[R11,R6]

      AND R2,R1, #0x1
      MOV R0,R2,LSL #2
      AND R2,R1,#0xE
      ORR R0, R0, R2,LSL #3
      AND R2, R1, #0xF0
      ORR R0,R0,R2,LSL #4   ;ro stores 12 bits with 0 in check bits

     

      MOV R5,#0       ;check pos1
      MOV R3,R0, LSR #2
      EOR R5,R5,R3

      MOV R3,R0, LSR #4
      EOR R5,R5,R3    
      MOV R3,R0, LSR #6
      EOR R5,R5,R3
      MOV R3,R0, LSR #8
      EOR R5,R5,R3
      MOV R3,R0, LSR #10
      EOR R5,R5,R3
      AND R5,R5, #0x1
      ORR R0,R0,R5

      MOV R5,#0      ;checkpos 2
      MOV R3,R0, LSR #1
      EOR R5,R5,R3    
      MOV R3,R0, LSR #4
      EOR R5,R5,R3
      MOV R3,R0, LSR #5
      EOR R5,R5,R3
      MOV R3,R0, LSR #8
      EOR R5,R5,R3
      MOV R3,R0, LSR #9
      EOR R5,R5,R3
      AND R5,R5, #0x2
      ORR R0,R0,R5

 
      MOV R5,#0      ;checkpos 4
      MOV R3,R0, LSR #1
      EOR R5,R5,R3
      MOV R3,R0, LSR #2
      EOR R5,R5,R3
      MOV R3,R0, LSR #3
      EOR R5,R5,R3
      MOV R3,R0, LSR #8
      EOR R5,R5,R3
      AND R5,R5, #0x8
      ORR R0,R0,R5
     

      MOV R5,#0     ;checkpos 8
      MOV R3,R0, LSR #1
      EOR R5,R5,R3
      MOV R3,R0, LSR #2
      EOR R5,R5,R3
      MOV R3,R0, LSR #3
      EOR R5,R5,R3
      MOV R3,R0, LSR #4
      EOR R5,R5,R3
      AND R5,R5, #0x80
      MOV R10,R0
      ORR R10,R10,R5
	  
	  STR R10,[R8,R7]
	  ADD R6,R6,#2
	  ADD R7,R7,#4
	  B ENCODE

	  
                       
DECODE CMP R1,R4     ; Decodes the encoded bits encoded using hamming (12,8)
	   
	  MOVEQ R12,R1
	  BEQ PreDecrypt
	  MUL R7,R4,R3
	  LDR R10,[R8,R7]

	LDR R9,=0XF80;1111 1000 0000
	AND R5,R10,R9;
	MOV R2,#0;
	MOV R6,#0;
LOOP1 AND R12,R5,#1;GETTING THE LAST BIT
     EOR R2,R2,R12;XORING EACH BIT (Ax0=A AND AX0=~A)
	 LSR R5,R5,#1;
	 CMP R5,#0;BREAKING WHEN THE VALUE BECOMES ZERO
	 BNE LOOP1
	 EOR R6,R6,R2;UPDATING ERROR NUMBER
	 LSL R6,R6,#1;SHIFTING TO LEFT 
	
	LDR R9,=0x878;1000 0111 1000
	AND R5,R10,R9;
	MOV R2,#0;
LOOP2 AND R12,R5,#1;
     EOR R2,R2,R12;
	 LSR R5,R5,#1;
	 CMP R5,#0;
	 BNE LOOP2
	 EOR R6,R6,R2;
	 LSL R6,R6,#1;
	
	LDR R9,=0X666;0110 0110 0110
	AND R5,R10,R9;
	MOV R2,#0;
LOOP3 AND R12,R5,#1;
     EOR R2,R2,R12;
	 LSR R5,R5,#1;
	 CMP R5,#0;
	 BNE LOOP3
	 EOR R6,R6,R2;
	 LSL R6,R6,#1;
	 
	LDR R9,=0X555;0101 0101 0101
	AND R5,R10,R9;
	MOV R2,#0;
LOOP4 AND R12,R5,#1;
     EOR R2,R2,R12;
	 LSR R5,R5,#1;
	 CMP R5,#0;
	 BNE LOOP4
	 EOR R6,R6,R2;R6 HAS THE FINAL ERROR POSITION VALUE
	 EOR R10,R10,R6;CORRECTING THE ERROR
	 LSR R10,R10,#2;REMOVING THE LAST TWO PARITY BITS
	 AND R5,R10,#1;EXTRACTING LAST BIT(I.E ACTUAL 3RD BIT OF 12 BITS)
	 LSR R10,R10,#1;SHIFTING TO RIGHT
	 ORR R12,R10,#1;MAKING LAST BIT AS 1
	 EOR R10,R12,#1;MAKING LAST BIT AS 0
	 ADD R10,R10,R5;
	 
	 AND R5,R10,#0XF;EXTRACTING LAST 4 BITS(I.E ACTUAL 3,5,6,7 BITS OF 12 BITS)
	 LSR R10,R10,#1;SHIFTING TO RIGHT
	 ORR R12,R10,#0XF;MAKING 4TH LAST BIT AS 1
	 EOR R10,R12,#0XF;MAKING 4TH LAST BIT AS 0
	 ADD R10,R10,R5;
	 ADD R9,R4,#80
	 STRH R10,[R8,R9]
	 ADD R4,R4,#2
	 B DECODE
	 
PreDecrypt MOV R9,#2  ;Setting appropriate registers,and fetching the key
	  SDIV R12,R12,R9
	  MOV R6,#0
	  SUB R11,R11,#30
	  ADD R3,R11,#21
	  LDR R10,[R3]
Decrypt CMP R12,R6
		MOVEQ R6,#0
		ADDEQ R5,R8,#120
		BEQ print
		MUL R7,R6,R9
		ADD R3, R8, #80;
		LDRH R4,[R3,R7]
		MOV R3,r4
		EOR R4,R10
		MOV R10,R3
		ADD R3,R8,#120
		STRH R4,[R3,R7]
		ADD R6,R6,#1
		B Decrypt
 
print CMP R12,R6 ; This section compares the input and output, and prints 1 if they are equal (which they should be) 0 otherwise(meaning the module is faulty)
	BEQ STOP
	MUL R7, R6,R9
	LDRH R4,[R11,R7]
	LDRH R3,[R5,R7]
	CMP R4,R3
	MOVEQ R0,#1 ;1 means input=output			
	MOVNE R0,#0			
	BL printMsg
	ADD R6,R6,#1
	B print
STOP B STOP                      

endfunc                    
END