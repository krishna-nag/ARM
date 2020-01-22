import ast
## Author: Krishna Nagaraja ##############################################
######################## MEMORY ##########################################
##########################################################################
# print (ast.dump(ode))
init_addr=0x20000000
end_addr= 0x20007FFF

temp_init=0xE0000080
temp_end=0xE0000FFF 
var={}
### program memory, for internal operations
mem={}
x=[i for i in range(init_addr,end_addr,4)]
for i in x:
	mem[i]=True #True implies memory is available for use


### temporary memory, for internal operations
temp={}
x=[i for i in range(temp_init,temp_end,4)]
for i in x:
	temp[i]=True #True implies memory is available for use

### registers
reg={}
x=["R"+str(i) for i in range(12)]
for i in x:
	reg[i]=True #True means available

### float registers
freg={}
x=["S"+str(i) for i in range(31)]
for i in x:
	freg[i]=True #True means available
Ifno=0
######################## MEMORY ##########################################
##########################################################################
def get_regs(n):
	l=[i for i in reg.keys() if(reg[i])]
	regs=[]
	for i in range(n):
		regs.append(l[i])
		reg[l[i]]=False
	return regs
def get_fregs(n):
	l=[i for i in freg.keys() if(freg[i])]
	fregs=[]
	for i in range(n):
		fregs.append(l[i])
		freg[l[i]]=False
	return fregs
def get_temp(n):
	l=[i for i in temp.keys() if(temp[i])]
	temps=[]
	for i in range(n):
		temps.append(l[i])
		temp[l[i]]=False
	if(n==1):
		return temps[0]
	else:
		return temps

def release_regs(regs):
	if(type(regs)==list):
		for i in regs:
			if(i[0]=='S'):
				freg[i]=True
			else:
				reg[i]=True
	else:
		if(regs[0]=='S'):
				freg[regs]=True
		else:
				reg[regs]=True

def release_temp(t):
	if(type(t)==list):
		for i in t:
			temp[i]=True
	else:
		temp[t]=True

def address(name,fun):
	if(fun=="main"):
		return var[name]["addr"]
	else:
		return var[fun][name]["addr"]
def typee(name,fun):
	if(fun=="main"):
		return var[name]["type"]
	else:
		return var[fun][name]["type"]

def allocate(name,fun,typ,l=0):
	l=[i for i in mem.keys() if(mem[i])]
	memm=l[0]
	mem[memm]=False
	if(fun=="main"):
		var[name]={}
		var[name]["addr"]=memm
		var[name]["type"]=typ
		if(l):
			var[name]["l"]=l
	else:
		var[fun][name]={}
		var[fun][name]["addr"]=memm
		var[fun][name]["type"]=typ
		if(l):
			var[fun][name]["l"]=l
	return memm

def isdeclared(name,fun):
	if(fun=="main"):
		if(name in var.keys()):
			return True
		else:
			return False
	else:
		if(name in var[fun].keys()):
			return True
		else:
			return False
def update_type(name,fun,typ):
	if(fun=="main"):
		var[name]["type"]=typ
	else:
		var[fun][name]["type"]=typ




def get_values(value,fun):
		ass_code=""
		#handling left value
		left_type=0
		left_value=0 #left value in regs[0], or fregs[0]
		right_type=0
		right_value=0 #left value in regs[0], or fregs[0]
		right_l=0
		left_l=0
		if(type(value.left)==ast.Name):

			if(isdeclared(value.left.id,fun)):
				addr=address(value.left.id,fun)
				typ=typee(value.left.id,fun)
			else:
				raise Exception(value.left.id+" not declared")
			if(typ==int):
				regs=get_regs(2)
				ass_code=ass_code+"\n"+"LDR "+regs[1]+",="+str(addr)+"\n"+"LDR "+regs[0]+",["+regs[1]+"]"
				release_reg(regs[1])
				#now regs[0] will have the l value
				left_type=int
				left_value=regs[0]
			elif(typ == float):
				fregs=get_fregs(1)
				regss=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regss[0]+",="+str(addr)+"\n"+"VLDR.F32 "+fregs[0]+" ,["+regss[0]+"]"
				release_regs(regss[0])
				#now fregs[0] will have the l value
				left_type=float
				left_value=fregs[0]
			elif(typ == str):
				left_value=addr
				left_type=str
			else:
				raise Exception(value.left.id+" is something which is invalid")



		elif(type(value.left) == ast.Num):
			if(type(value.left.n) == int):
				regs=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regs[0]+",="+str(value.left.n) #we now have left value in Regs[0]
				left_type=int
				left_value=regs[0]
			elif(type(value.left.n) == float):
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+"VLDR.F32 "+fregs[0]+",="+str(value.left.n) #we now have left value in Regs[0]
				left_type=float
				left_value=fregs[0]
			else:
				raise Exception(value.left.n+" is something which is invalid")
		elif(type(value.left) == ast.Str):
			s=value.left.s
			l=len(s)
			addr=get_temp(l/4) #l contigous bytes
			regs=get_regs(2)
			for i in range(l):
				ass_code=ass_code+"\n"+"LDR "+regs[0]+",="+str(addr)+"\n"+"LDR "+regs[1]+",="+str(ord(s[i]))+"\n"+"STRB "+regs[1]+", ["+regs[0]+"]"
				addr=addr+1
			release_regs(regs)
			left_value=addr
			left_type=str
			left_l=l
		else:
			typ,assem,addr,l=evaluate(value.left,fun)
			if(typ==str):
				left_type=typ
				left_value=addr
				left_l=l
			elif(typ==float):
				regs=get_regs(1)
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[0]+",="+str(addr)+"\n"+\
				"VLDR.F32 "+fregs[0]+" ,["+regs[0]+"]"
				left_type=typ
				release_regs(regs)
				left_value=fregs[0]
			else:
				regs=get_regs(2)
				#LDR r(1),=addr
				#LDR r(0),[r(1)]
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[1]+",="+str(addr)+"\n"+\
				"LDR "+regs[0]+",["+regs[1]+"]"
				left_value=regs[0]
				release_temp(addr)
				release_regs(regs[1])
				left_type=typ

		#By now, we have l value with us, now r value

		if(type(value.right)==ast.Name):
			if(isdeclared(value.right.id,fun)):
				addr=address(value.right.id,fun)
				typ=typee(value.right.id,fun)
			else:
				raise Exception(value.right.id+" not declared")
			if(typ==int):
				regs=get_regs(2)
				ass_code=ass_code+"\n"+"LDR "+regs[1]+",="+str(addr)+"\n"+"LDR "+regs[0]+",["+regs[1]+"]"
				release_regs(regs[1])
				#now regs[0] will have the l value
				right_type=int
				right_value=regs[0]
			elif(typ == float):
				fregs=get_fregs(1)
				regss=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regss[0]+",="+str(addr)+"\n"+"VLDR.F32 "+fregs[0]+" ,["+regss[0]+"]"
				release_regs(regss[0])
				#now fregs[0] will have the l value
				right_type=float
				right_value=fregs[0]
			elif(typ == str):
				right_value=addr
				right_type=str
			else:
				raise Exception(value.right.id+" is something which is invalid")


		elif(type(value.right) == ast.Num):
			if(type(value.right.n) == int):
				regs=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regs[0]+",="+str(value.right.n) #we now have right value in Regs[0]
				right_type=int
				right_value=regs[0]
			elif(type(value.right.n) == float):
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+"VLDR.F32 "+fregs[0]+",="+str(value.right.n) #we now have right value in Regs[0]
				right_type=float
				right_value=fregs[0]
			else:
				raise Exception(value.right.n+" is something which is invalid")
		elif(type(value.right) == ast.Str):
			s=value.right.s
			l=len(s)
			addr=get_temp(l/4) #l contigous bytes
			regs=get_regs(2)
			for i in range(l):
				ass_code=ass_code+"\n"+"LDR "+regs[0]+",="+str(addr)+"\n"+"LDR "+regs[1]+",="+str(ord(s[i]))+"\n"+"STRB "+regs[1]+", ["+regs[0]+"]"
				addr=addr+1
			release_regs(regs)
			right_value=addr
			right_type=str
			right_l=l
		else:
			typ,assem,addr,l=evaluate(value.right,fun)
			if(typ==str):
				right_type=typ
				right_value=addr
				right_l=l
			else:
				regs=get_regs(2)
				#LDR r(1),=addr
				#LDR r(0),[r(1)]
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[1]+",="+str(addr)+"\n"+\
				"LDR "+regs[0]+",["+regs[1]+"]"
				right_value=regs[0]
				release_temp(addr)
				release_regs(regs[1])
				right_type=typ

		#Now we have both l and r value
		return left_value,left_type,left_l,right_value,right_type,right_l,ass_code


def operate(lvalue,rvalue,left_type,right_type,op,ass_code):
	if(left_type==int and right_type==int):
				#ADD lvalue,lvalue,rvalue
				#STR lvalue,[addr]
				#now return the temp address
				addr=get_temp(1)
				ass_code=ass_code+"\n"+op+" "+lvalue+","+lvalue+","+rvalue+"\n"+"LDR "+rvalue+",="+str(addr)+"\n"+"STR "+lvalue+","+"["+rvalue+"]"
				release_regs([lvalue,rvalue])

				return int,ass_code,addr,False
	elif(left_type==int and right_type==float):
				#VMOV.F32 s$,lvalue
				#VCVT.F32.S32 S$,S$	 
				#VADD.F s$,s$,rvalue
				#VMOV.F32 lvalue,s$
				#LDR r$,=addr
				#STR lvalue,[r$]

				#now return the temp address
				fregs=get_fregs(1)
				addr=get_temp(1)
				regs=get_regs(1)
				ass_code=ass_code+"\n"\
				+"VMOV.F32 "+fregs[0]+","+lvalue+"\n"\
				+"VCVT.F32.S32 "+fregs[0]+", "+fregs[0]+"\n"\
				+"V"+op+".F "+fregs[0]+","+fregs[0]+","+rvalue+"\n"\
				+"VMOV.F32 "+lvalue+", "+fregs[0]+"\n"\
				+"LDR "+regs[0]+", "+"="+str(addr)+"\n"\
				+"STR "+lvalue+", ["+regs[0]+"]"

				release_regs([lvalue,rvalue])
				release_regs(fregs)
				release_regs(regs)
				return float,ass_code,addr,False
	elif(left_type==float and right_type==int):
				#VMOV.F32 s$,rvalue	 
				#VCVT.F32.S32 S$,S$	 
				#VADD.F s$,s$,lvalue
				#VMOV.F32 rvalue,s$
				#LDR r$,=addr
				#STR rvalue,[r$]

				#now return the temp address
				fregs=get_fregs(1)
				addr=get_temp(1)
				regs=get_regs(1)
				ass_code=ass_code+"\n"\
				+"VMOV.F32 "+fregs[0]+","+rvalue+"\n"\
				+"VCVT.F32.S32 "+fregs[0]+", "+fregs[0]+"\n"\
				+"V"+op+".F "+fregs[0]+","+fregs[0]+","+lvalue+"\n"\
				+"VMOV.F32 "+rvalue+", "+fregs[0]+"\n"\
				+"LDR "+regs[0]+", "+"="+str(addr)+"\n"\
				+"STR "+rvalue+", ["+regs[0]+"]"

				release_regs([lvalue,rvalue])
				release_regs(fregs)
				release_regs(regs)

				return float,ass_code,addr,False
	elif(left_type==float and right_type==float):	 
				#VADD.F rvalue,lvalue,rvalue
				#LDR r$,=addr
				#VMOV.F r1$,rvalue
				#STR r1$,[r$]

				#now return the temp address
				addr=get_temp(1)
				regs=get_regs(2)
				ass_code=ass_code+"\n"\
				+"V"+op+".F "+rvalue+","+lvalue+","+rvalue+"\n"\
				+"LDR "+regs[0]+", "+"="+str(addr)+"\n"\
				+"VMOV.F "+regs[1]+", "+rvalue+"\n"\
				+"STR "+regs[1]+", ["+regs[0]+"]"

				release_regs(regs)
				release_regs([lvalue,rvalue])
				return float,ass_code,addr,False
	else:
				raise Exception("operation not supported")

def get_comp_values(value,fun):
		left_value=0
		right_value=0
		left_type=0
		right_type=0
		ass_code=""
		if(type(value.left)==ast.Name):

			if(isdeclared(value.left.id,fun)):
				addr=address(value.left.id,fun)
				typ=typee(value.left.id,fun)
			else:
				raise Exception(value.left.id+" not declared")
			if(typ==int):
				regs=get_regs(2)
				ass_code=ass_code+"\n"+"LDR "+regs[1]+",="+str(addr)+"\n"+"LDR "+regs[0]+",["+regs[1]+"]"
				release_reg(regs[1])
				#now regs[0] will have the l value
				left_type=int
				left_value=regs[0]
			elif(typ == float):
				fregs=get_fregs(1)
				regss=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regss[0]+",="+str(addr)+"\n"+"VLDR.F32 "+fregs[0]+" ,["+regss[0]+"]"
				release_regs(regss[0])
				#now fregs[0] will have the l value
				left_type=float
				left_value=fregs[0]
			else:
				raise Exception(value.left.id+" is something which is invalid")

		elif(type(value.left) == ast.Num):
			if(type(value.left.n) == int):
				regs=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regs[0]+",="+str(value.left.n) #we now have left value in Regs[0]
				left_type=int
				left_value=regs[0]
			elif(type(value.left.n) == float):
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+"VLDR.F32 "+fregs[0]+",="+str(value.left.n) #we now have left value in Regs[0]
				left_type=float
				left_value=fregs[0]
			else:
				raise Exception(value.left.n+" is something which is invalid")
		else:
			typ,assem,addr,l=evaluate(value.left,fun)
			if(typ==float):
				regs=get_regs(1)
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[0]+",="+str(addr)+"\n"+\
				"VLDR.F32 "+fregs[0]+" ,["+regs[0]+"]"
				left_type=typ
				release_regs(regs)
				left_value=fregs[0]
			else:
				regs=get_regs(2)
				#LDR r(1),=addr
				#LDR r(0),[r(1)]
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[1]+",="+str(addr)+"\n"+\
				"LDR "+regs[0]+",["+regs[1]+"]"
				left_value=regs[0]
				release_temp(addr)
				release_regs(regs[1])
				left_type=typ

		if(type(value.comparators[0])==ast.Name):

			if(isdeclared(value.comparators[0].id,fun)):
				addr=address(value.comparators[0].id,fun)
				typ=typee(value.comparators[0].id,fun)
			else:
				raise Exception(value.comparators[0].id+" not declared")
			if(typ==int):
				regs=get_regs(2)
				ass_code=ass_code+"\n"+"LDR "+regs[1]+",="+str(addr)+"\n"+"LDR "+regs[0]+",["+regs[1]+"]"
				release_reg(regs[1])
				#now regs[0] will have the l value
				right_type=int
				right_value=regs[0]
			elif(typ == float):
				fregs=get_fregs(1)
				regss=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regss[0]+",="+str(addr)+"\n"+"VLDR.F32 "+fregs[0]+" ,["+regss[0]+"]"
				release_regs(regss[0])
				#now fregs[0] will have the l value
				right_type=float
				right_value=fregs[0]
			else:
				raise Exception(value.left.id+" is something which is invalid")

		elif(type(value.comparators[0]) == ast.Num):
			if(type(value.comparators[0].n) == int):
				regs=get_regs(1)
				ass_code=ass_code+"\n"+"LDR "+regs[0]+",="+str(value.comparators[0].n) #we now have left value in Regs[0]
				right_type=int
				right_value=regs[0]
			elif(type(value.comparators[0].n) == float):
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+"VLDR.F32 "+fregs[0]+",="+str(value.comparators[0].n) #we now have left value in Regs[0]
				right_type=float
				right_value=fregs[0]
			else:
				raise Exception(value.comparators[0].n+" is something which is invalid")
		else:
			typ,assem,addr,l=evaluate(value.comparators[0],fun)
			if(typ==float):
				regs=get_regs(1)
				fregs=get_fregs(1)
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[0]+",="+str(addr)+"\n"+\
				"VLDR.F32 "+fregs[0]+" ,["+regs[0]+"]"
				right_type=typ
				release_regs(regs)
				right_value=fregs[0]
			else:
				regs=get_regs(2)
				#LDR r(1),=addr
				#LDR r(0),[r(1)]
				ass_code=ass_code+"\n"+assem+"\n"+\
				"LDR "+regs[1]+",="+str(addr)+"\n"+\
				"LDR "+regs[0]+",["+regs[1]+"]"
				right_value=regs[0]
				release_temp(addr)
				release_regs(regs[1])
				right_type=typ
		return left_value,left_type,right_value,right_type,ass_code
def compare(left_value,right_value,left_type,right_type,op,opinv):
	ass_code=""
	if(left_type==int and right_type==int):
		#CMP leftvalue,rightvalue
		#MOVop R0,#0xFFFFFFFF
		#MOVopinv R0,#0x00000000
		#LDR R1,=temp_addr
		#STR R0,[R1]
		regs=get_regs(2)
		addr=get_temp(1)
		ass_code=asscode+"\n"+\
		"CMP "+left_value+" "+right_value+"\n"+\
		"MOV"+op+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"MOV"+opinv+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"LDR "+regs[1]+",="+str(addr)+"\n"+\
		"STR "+regs[0]+", ["+regs[1]+"]"+"\n"
		release_regs(regs)
		release_regs([left_value,right_value])
		return bool,ass_code,addr,0
	elif(left_type==int and right_type==float):
		#VMOV.F32 s$,lvalue	 
		#VCVT.F32.S32 S$,S$	 
		#VCMP.F s$,rvalue
		#VMRS APSR_nzcv,FPSCR
		#MOVop R0,#0xFFFFFFFF
		#MOVopinv R0,#0x00000000
		#LDR r$,=addr
		#STR r0,[r$]
		regs=get_regs(2)
		fregs=get_fregs(1)
		addr=get_temp(1)
		ass_code=asscode+"\n"+\
		"VMOV.F32 "+fregs[0]+","+left_value+"\n"+\
		"VCVT.F32.S32 "+fregs[0]+", "+fregs[0]+"\n"+\
		"VCMP.F "+fregs[0]+" "+right_value+"\n"+\
		"VMRS APSR_nzcv,FPSCR\n"+\
		"MOV"+op+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"MOV"+opinv+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"LDR "+regs[1]+",="+str(addr)+"\n"+\
		"STR "+regs[0]+", ["+regs[1]+"]"+"\n"
		release_regs(regs)
		release_regs(fregs)
		release_regs([left_value,right_value])
		return bool,ass_code,addr,0
	elif(left_type==float and right_type==int):
		#VMOV.F32 s$,rvalue	 
		#VCVT.F32.S32 S$,S$	 
		#VCMP.F lvalue,s$
		#VMRS APSR_nzcv,FPSCR
		#MOVop R0,#0xFFFFFFFF
		#MOVopinv R0,#0x00000000
		#LDR r$,=addr
		#STR r0,[r$]
		regs=get_regs(2)
		fregs=get_fregs(1)
		addr=get_temp(1)
		ass_code=asscode+"\n"+\
		"VMOV.F32 "+fregs[0]+","+right_value+"\n"+\
		"VCVT.F32.S32 "+fregs[0]+", "+fregs[0]+"\n"+\
		"VCMP.F "+left_value+" "+fregs[0]+"\n"+\
		"VMRS APSR_nzcv,FPSCR\n"+\
		"MOV"+op+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"MOV"+opinv+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"LDR "+regs[1]+",="+str(addr)+"\n"+\
		"STR "+regs[0]+", ["+regs[1]+"]"+"\n"
		release_regs(regs)
		release_regs(fregs)
		release_regs([left_value,right_value])
		return bool,ass_code,addr,0
	elif(left_type==float and right_type==float):
		#VCMP.F lvalue,rvalue
		#VMRS APSR_nzcv,FPSCR
		#MOVop R0,#0xFFFFFFFF
		#MOVopinv R0,#0x00000000
		#LDR r$,=addr
		#STR r0,[r$]
		regs=get_regs(2)
		addr=get_temp(1)
		ass_code=asscode+"\n"+\
		"VCMP.F "+left_value+" "+right_value+"\n"+\
		"VMRS APSR_nzcv,FPSCR\n"+\
		"MOV"+op+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"MOV"+opinv+" "+regs[0]+", 0xFFFFFFFF"+"\n"+\
		"LDR "+regs[1]+",="+str(addr)+"\n"+\
		"STR "+regs[0]+", ["+regs[1]+"]"+"\n"
		release_regs(regs)
		release_regs([left_value,right_value])
		return bool,ass_code,addr,0



####################################################################################################################################
def compilee(tree,body,fun):
	ass_code=""
	end_code=""
	if(type(tree)==ast.Module):
			return compilee(tree.body,1,fun)
	elif(type(tree)==ast.If):
			#eval test
			s1=compilee(tree.body,1,fun)
			typ,assem,addr,l=evaluate(tree.test,fun)
			orelses_body=[]
			orelses_test=[]
			temp=tree.orelse
			while(1):
				if(len(temp)==0):
					break
				elif(type(temp[0])==ast.If):
					asscode,endcode=compilee(temp.orelse[0].body,1,fun)
					orelses_body.append(asscode)
					end_code=end_code+"\n"+endcode
					typ1,assem1,addr1,l1=evaluate(temp.orelse[0].test,fun)
					orelses_test.append([assem1,addr1])
					temp=temp.orelse[0].orelse
				else:
					#this means there is an else
					asscode,endcode=compilee(temp,1,fun)
					break
			ass_code=ass_code+"\n"+\
			"LDR "+regs[0]+",="+str(addr)+"\n"+\
			"LDR "+regs[1]+",["+regs[0]+"]"+"\n"+\
			"LDR "+regs[2]+",=0xFFFFFFFF"+"\n"+\
			"CMP "+regs[1]+","+regs[2]+"\n"+\
			"BLEQ "+"IF"+str(Ifno)
			for i in range(orelses_body):
				ass_code=ass_code+"\n"+\
				"LDR "+regs[0]+",="+str(orelses_test[i][0])

			#LDR R0,=addr
			#LDR R1,[R0]
			#LDR R2,=0xFFFFFFFF
			#CMP R1,R2
			#BLEQ Ifn
			#LOOP
			#LDR R0,=addr
			#LDR R1,[R0]
			#CMP R1,R2
			#BLEQ elifn


	elif(type(tree)== list and body):
			if(fun!="main"):
				var[fun]={}
			arr=[]
			endd=[]
			for i in range(len(tree)):
				ass_code,end_code=compilee(tree[i],0,fun)
				arr.append(ass_code)
				endd.append(end_code)
			return "\n".join(arr),"\n".join(endd)
	elif(type(tree)== ast.Assign):
		#calculate value, and determine its type
		typ,assem,addr,l=evaluate(tree.value,fun)
		#target is going to be straight forward
		if(isdeclared(tree.targets[0].id,fun)):
			addre=address(tree.targets[0].id,fun)
			update_type(tree.targets[0].id,fun,float) 
		else:
			addre=allocate(tree.targets[0].id,fun,typ,l)
		#LDR R0,=addre
		#LDR R1,=addr
		#LDR R2,[R1]
		#STR R2,[R0]
		regs=get_regs(3)
		release_temp(addr)
		release_regs(regs)
		ass_code=ass_code+"\n"+assem+"\n"+\
		"LDR "+regs[0]+",= "+str(addre)+"\n"+\
		"LDR "+regs[1]+",= "+str(addr)+"\n"+\
		"LDR "+regs[2]+", ["+regs[1]+"] \n"+\
		"STR "+regs[2]+", ["+regs[0]+"]"
		return ass_code,end_code





def evaluate(value,fun):
	ass_code=""
	if(type(value) == ast.Num):
		if(type(value.n)==int):	
			#LDR R0,=num
			#LDR R1,=addr
			#STR R0,[R1]
			regs=get_regs(2)
			addr=get_temp(1)
			ass_code=ass_code+"\n"+\
			"LDR "+regs[0]+",="+str(value.n)+"\n"+\
			"LDR "+regs[1]+",="+str(addr)+"\n"+\
			"STR "+regs[0]+", ["+regs[1]+"]"
			release_regs(regs)
			return type(value.n),ass_code,addr,0
		elif(type(value.n)==float):
			#VLDR.F32 s0,=num
			#VMOV.F R0,s0
			#LDR R1,=addr
			#STR R0,[R1]
			fregs=get_fregs(1)
			regs=get_regs(2)
			addr=get_temp(1)
			ass_code=ass_code+"\n"+\
			"VLDR.F32 "+fregs[0]+",="+str(value.n)+"\n"+\
			"VMOV.F "+regs[0]+", "+fregs[0]+"\n"+\
			"LDR "+regs[1]+",="+str(addr)+"\n"+\
			"STR "+regs[0]+", ["+regs[1]+"]"
			release_regs(regs)
			release_regs(fregs)
			return type(value.n),ass_code,addr,0
		else:
			raise Exception(str(value.n)+" type not supported")

	elif(type(value) == ast.Str):
		#LDR R0,=ord(value.s)
		#LDR R1,=addr
		#STR R0,[R1]
		regs=get_regs(2)
		addr=get_temp(1)
		ass_code=ass_code+"\n"+\
		"LDR "+regs[0]+",="+str(ord(value.s))+"\n"+\
		"LDR "+regs[1]+",="+str(addr)+"\n"+\
		"STR "+regs[0]+", ["+regs[1]+"]"
		release_regs(regs)
		return type(value.s),ass_code,addr,0
	elif(type(value) == ast.BinOp):
		
		#handling left value
		left_type=0
		left_value=0 #left value in regs[0], or fregs[0]
		right_type=0
		right_value=0 #left value in regs[0], or fregs[0]
		lvalue,left_type,left_l,rvalue,right_type,right_l,ass_code=get_values(value,fun)

		if(type(value.op)==ast.Add):
			return operate(lvalue,rvalue,left_type,right_type,"ADD",ass_code)
		elif(type(value.op)==ast.Sub):
			return operate(lvalue,rvalue,left_type,right_type,"SUB",ass_code)
		elif(type(value.op)==ast.Mult):
			return operate(lvalue,rvalue,left_type,right_type,"MUL",ass_code)
		elif(type(value.op)==ast.Div):
			return operate(lvalue,rvalue,left_type,right_type,"DIV",ass_code)
		elif(type(value.op)==ast.Mod):
			if(left_type==int and right_type==int):
				#MOD lvalue,lvalue,rvalue
				#STR lvalue,[addr]
				#now return the temp address
				addr=get_temp(1)
				ass_code=ass_code+"\n"+"MOD"+" "+lvalue+","+lvalue+","+rvalue+"\n"+"LDR "+rvalue+",="+str(addr)+"\n"+"STR "+lvalue+","+"["+rvalue+"]"
				release_regs([lvalue,rvalue])

				return int,ass_code,addr,False
			else:
				raise Exception("operation not valid")

	elif(type(value) == ast.Compare):
		#True = FFFFFFFF
		#False = 00000000
		left_value,left_type,right_value,right_type=get_comp_values(value,fun)
		if(type(value.ops[0])==ast.Lt):
			return compare(left_value,right_value,left_type,right_type,"LT","GE")
		elif(type(value.ops[0])==ast.Gt):
			return compare(left_value,right_value,left_type,right_type,"GT","LE")
		elif(type(value.ops[0])==ast.LtE):
			return compare(left_value,right_value,left_type,right_type,"LE","GT")
		elif(type(value.ops[0])==ast.GtE):
			return compare(left_value,right_value,left_type,right_type,"GE","LT")
		elif(type(value.ops[0])==ast.Eq):
			return compare(left_value,right_value,left_type,right_type,"EQ","NE")
		elif(type(value.ops[0])==ast.NotEq):
			return compare(left_value,right_value,left_type,right_type,"NE","EQ")
		else:
			raise Exception("operation not valid")


	elif(type(value) == ast.BoolOp):
		pass
	else:
		raise Exception("not supported")

ff=input("Enter file name:")
c=open(ff).read()
ode=ast.parse(c)
x,y=compilee(ode,0,"main")
# print x

# print(x)
# print([' '*4 + i for i in x.split('\n')])
print('''
  area appcode, CODE, READONLY
  export __main
  ENTRY
__main function
	''')
print('\n'.join([' '*4 + i for i in x.split('\n')]))
print "END"
