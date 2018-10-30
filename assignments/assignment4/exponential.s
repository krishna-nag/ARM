;PRESERVE8
;Krishna Nagaraja
;IMT2015512

	THUMB
	AREA 	appcode, CODE, READONLY
	export __main
	ENTRY
__main function
	VMOV.F s0, #6.5 ; x in for e^x
	VMOV.F s1, #1 ;current sum and result
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
	
	
	
stop B stop ; stop program
	endfunc
	end
;TESTING
;INPUT=s0
;OUTPUT=s1
; s0=1, s1=2.71828 : passed
; s0=-1, s1=0.367879 :passed
; s0=-2, s1=0.135335  :passed
; s0=-1.5, s1= 0.22313 :passed
; s0=6.5, s1=665.141633 :passed
	