    ;Krishna Nagaraja
	THUMB
	AREA 	appcode, CODE, READONLY
	IMPORT printMsg             
	export __main
	ENTRY
	; Registers=>
	; s9=w0
	; s10=w1
	; s11=w2
	; s12=bias
	; s13 to s15=input1=100
	; s16 to s18=input2=101
	; s19 to s21=input3=110
	; s22 to s24=input4=111
	; output= 0001011111000110011011101000 (printed in  printf window)
	; This matches with the output of the python program, but some gates are not functioning the way they should
	; even in the python program.
	
__main function
	;inputs
	VLDR.F32 s13,=1
	VLDR.F32 s14,=0
	VLDR.F32 s15,=0
	VLDR.F32 s16,=1
	VLDR.F32 s17,=0
	VLDR.F32 s18,=1
	VLDR.F32 s19,=1
	VLDR.F32 s20,=1
	VLDR.F32 s21,=0
	VLDR.F32 s22,=1
	VLDR.F32 s23,=1
	VLDR.F32 s24,=1
	
	;AND
	BL set_and
	BL process
	;OR
	BL set_or
	BL process
	;NOT
	BL set_not
	BL process
	;XOR
	BL set_xor
	BL process
	;XNOR
	BL set_xnor
	BL process
	;NAND
	BL set_nand
	BL process
	;NOR
	BL set_nor
	BL process
	
mainstop B mainstop ; stop program
	endfunc

;;AND
set_and VLDR.F32 s9,=-0.1	
	VLDR.F32 s10,=0.2
	VLDR.F32 s11, =0.2
	VLDR.F32 s12, =-0.2
	BX lr
;;OR
set_or VLDR.F32 s9,=-0.1	
	VLDR.F32 s10,=0.7
	VLDR.F32 s11, =0.7
	VLDR.F32 s12, =-0.1
	BX lr
;;NOT
set_not VLDR.F32 s9,=0.5	
	VLDR.F32 s10,=-0.7
	VLDR.F32 s11, =0
	VLDR.F32 s12, =0.1
	BX lr
;;XOR
set_xor VLDR.F32 s9,=-5	
	VLDR.F32 s10,=20
	VLDR.F32 s11, =10
	VLDR.F32 s12, =1
	BX lr
;;XNOR
set_xnor VLDR.F32 s9,=-5	
	VLDR.F32 s10,=20
	VLDR.F32 s11, =10
	VLDR.F32 s12, =1
	BX lr
;;NAND
set_nand VLDR.F32 s9,=0.6
	VLDR.F32 s10,=-0.8
	VLDR.F32 s11, =-0.8
	VLDR.F32 s12, =0.3
	BX lr
;;NOR
set_nor VLDR.F32 s9,=0.5	
	VLDR.F32 s10,=-0.7
	VLDR.F32 s11, =-0.7
	VLDR.F32 s12, =0.1
	BX lr
; process function performs the operation(decided by the weights and bias) on all inputs, and prints the output	
process VMUL.F32 S25, S13, S9	;dot product=(input[0]*w0+input[1]*w1+input[2]*w2) ;input1
		VFMA.F32 S25, S14, S10
		VFMA.F32 S25, S15, S11
		VADD.F32 S25, S25, S12	;add bias
		MOV R3,lr
		VMOV.F s0,s25 ; input to sigmoid
		BL sigmoid
		VMOV.F s4,#0.5		; if s4>0.5, logic=1, else logic=0
		VCMP.F s1, s4		
		VMRS APSR_nzcv,FPSCR
		MOVGE R0,#1			
		MOVLT R0,#0	
		BL printMsg
		;input 2
		VMUL.F32 S25, S16, S9	;dot product=(input[0]*w0+input[1]*w1+input[2]*w2) ;input1
		VFMA.F32 S25, S17, S10
		VFMA.F32 S25, S18, S11
		VADD.F32 S25, S25, S12	;add bias
		VMOV.F s0,s25 ; input to sigmoid
		BL sigmoid
		VMOV.F s4,#0.5		; if s4>0.5, logic=1, else logic=0
		VCMP.F s1, s4		
		VMRS APSR_nzcv,FPSCR
		MOVGE R0,#1			
		MOVLT R0,#0			
		BL printMsg
		;input 3
		VMUL.F32 S25, S19, S9	;dot product=(input[0]*w0+input[1]*w1+input[2]*w2) ;input1
		VFMA.F32 S25, S20, S10
		VFMA.F32 S25, S21, S11
		VADD.F32 S25, S25, S12	;add bias
		VMOV.F s0,s25 ; input to sigmoid
		BL sigmoid
		VMOV.F s4,#0.5		; if s4>0.5, logic=1, else logic=0
		VCMP.F s1, s4		
		VMRS APSR_nzcv,FPSCR
		MOVGE R0,#1			
		MOVLT R0,#0			
		BL printMsg
		;input 4
		VMUL.F32 S25, S22, S9	;dot product=(input[0]*w0+input[1]*w1+input[2]*w2) ;input1
		VFMA.F32 S25, S23, S10
		VFMA.F32 S25, S24, S11
		VADD.F32 S25, S25, S12	;add bias
		VMOV.F s0,s25 ; input to sigmoid
		BL sigmoid
		VMOV.F s4,#0.5		; if s4>0.5, logic=1, else logic=0
		VCMP.F s1, s4		
		VMRS APSR_nzcv,FPSCR
		MOVGE R0,#1			
		MOVLT R0,#0			
		BL printMsg
		MOV lr,R3
		BX lr

sigmoid VNEG.F s0, s0 ; s0=-s0 (s0 is input to sigmoid) also, input to exponential is s0 
	VMOV.F s1, #1 ;current sum and result ;s0 has input
	VMOV.F s2, #1; factorial current
	VMOV.F s3, #2 ;prevsum
	VMOV.F s4, #1 ;current term in the loop
	VMOV.F s5, #1 ;register to hold 1
	
	
loop	VCMP.F s1,s3
	VMRS APSR_nzcv, FPSCR
	BEQ stop
	VMOV.F s3,s1 ;prev=s1
	VMUL.F s4,s4,s0
	VDIV.F s4,s4,s2
	VADD.F s2,s2,s5
	VFMA.F s1,s4,s5
	B loop
stop 	VADD.F32 s1,s5,s1; s1=1+s1(s1 has value 1+e^-x)
	VDIV.F32 s1,s5,s1; s1=1/s1 
	VMOV.F32 R0,s1	 
	BX lr

	end