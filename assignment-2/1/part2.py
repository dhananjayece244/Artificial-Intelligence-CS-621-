#!/usr/bin/python3
import sys
import string


#predefined operators, values and variables
operator = ['+','*','f']
value = ['s','0']
variable = ['x','y']
l = 99999999
ptr = None
sys.setrecursionlimit(10000)


class Term(object):
	term_value = None
	left_child = None
	right_child = None
	def __init__(self,string):
		self.term_value = string[0]
		x = string[0]
		#for + and *
		if(x=='+' or x=='*'):
			k = findComma(string)
			left = string[2:k]
			right = string[k+1:-1]
			self.left_child = Term(left)
			self.right_child = Term(right)
		#for f
		elif(x=='f'):
			left = string[2:-1]
			self.left_child = Term(left)
			self.right_child = None
		#for s
		elif(x=='s'):
			left = string[2:-1]
			self.left_child = Term(left)
			self.right_child = None
		#for 0
		else:
			self.left_child = None
			self.right_child = None


#finds the actual position of comma for the corresponding + or *
def findComma(string):
	paren = 0
	for i in range(len(string)):
		if(string[i]=='('):
			paren += 1
		elif(string[i]==')'):
			paren -= 1
		else:
			pass
		if(paren==1 and string[i]==','):
			return i


#reads the rules file and replaces the fact with f
def openFile():
	#conver fact to f
	with open("rules.txt", "rt") as fin:
	    with open("new_rules.txt", "wt") as fout:
	        for line in fin:
	            fout.write(line.replace('fact', 'f'))
	#read the rules file
	with open("new_rules.txt") as f:
	    content = f.readlines()
	content = [x.strip() for x in content]
	return content 


#removes implies and make each rule a tree
def processRules(content):
	rhs = [] 
	lhs = []
	for i in content:
		a = i.rsplit(" ",2)
		x = Term(a[2])
		y = Term(a[0])
		rhs.append(x)
		lhs.append(y)
	return rhs,lhs	


#prints preorder traversal of the tree
def treePrint(count,root):
	if root:
		print(count," ", root.term_value)
		count=count+1
		treePrint(count,root.left_child)
		treePrint(count,root.right_child)


#is any of the defined operator is present in the tree
def isOperatorPresent(root):
	#start
	if root:
		if root.term_value in operator:
			return True
		else:
			return isOperatorPresent(root.left_child) or isOperatorPresent(root.right_child)
	return False


#find the rule no. that should be applied on the subtree
def findRule(subtree_ptr,lhs):
	
	root_val = subtree_ptr.term_value
	left_val = subtree_ptr.left_child.term_value
	for i in range(len(lhs)):
		r = lhs[i]
		v = r.term_value
		lv = r.left_child.term_value
		if(root_val==v and left_val==lv):
			return i
	return -1


#apply the rule and do unification
def applyRule(subtree,index,lhs,rhs):
	#start
	if(index==0):
		x=subtree.right_child
		subtree.term_value=x.term_value
		subtree.left_child=x.left_child
		subtree.right_child=None
		
	elif(index==1):
		x = subtree.left_child.left_child
		y = subtree.right_child
		r = rhs[index]
		temp=Term("0")
		temp.term_value=rhs[index].left_child.term_value
		temp.left_child=x
		temp.right_child=y
		subtree.term_value = rhs[index].term_value
		subtree.left_child=temp
		subtree.right_child=None
	
	elif(index==2):
		subtree.term_value=rhs[2].term_value
		subtree.left_child=rhs[2].left_child
		subtree.right_child=rhs[2].right_child
		
	elif(index==3):
		x = subtree.left_child.left_child
		y = subtree.right_child
		r = rhs[index]
		temp=Term("0")
		temp.term_value=r.right_child.term_value
		temp.left_child=x
		temp.right_child=y
		subtree.term_value=r.term_value
		subtree.left_child=y
		subtree.right_child=temp

	elif(index==4):
		r=rhs[4]
		subtree.term_value=r.term_value

	elif(index==5):
		l = subtree.left_child
		x = subtree.left_child.left_child
		r = rhs[index]
		temp = Term("0")
		temp.term_value=r.right_child.term_value
		temp.left_child=x
		temp.right_child=None
		subtree.term_value=r.term_value
		subtree.left_child=l
		subtree.right_child=temp

	if isOperatorPresent(subtree):
		replace_tree(subtree,lhs,rhs)


#replace subtree with new subtree formed by unification using rules and return the root of the tree
def replaceSubtree(subtree_ptr,lhs,rhs):
	#start
	index = findRule(subtree_ptr,lhs) #find the rule that to be applied on the subtree
	if(index!=-1):
		applyRule(subtree_ptr,index,lhs,rhs) #apply the rule and do the unification


def replace_tree(root,lhs,rhs):
	if root:
		replace_tree(root.left_child,lhs,rhs)
		replace_tree(root.right_child,lhs,rhs)
		if root.term_value in operator:
			replaceSubtree(root,lhs,rhs)


#evaluate a given expression with constants
def evaluateExp(inp_term):
	content = openFile()
	rhs,lhs = processRules(content)  #take each rule and divide it into two parts, lhs and rhs
	inp_term = inp_term.replace("fact","f")
	root = Term(inp_term) #convert the input term into tree
	replace_tree(root,lhs,rhs)
	return root


#print the values of variables for which the equation satisfies
def printSolution(dict_val,var):
	#pass
	print("-----------------")
	for i in var:
		c = dict_val[i]
		cs = makeS(c)
		print(i," = ",cs)
	print("-----------------")


#convert any integer in the form s(s(..(0)))
def makeS(c):
	s_num = ""
	for i in range(2*c):
		if(i%2==0):
			s_num += 's'
		else:
			s_num += '('
	s_num += '0'
	for i in range(c):
		s_num += ')'
	return s_num


#replace variables in lhs of the equation with values present in dict_val
def replaceVarWithVal(dict_val,var,eq):
	for i in var:
		a = dict_val[i]
		eq = eq.replace(i,a)
	return eq 


#given s(s(...(0))) in tree form, append all the s in a list and return it
def treeToNum(root,lst):
	if root:
		lst.append(root.term_value)
		treeToNum(root.left_child,lst)
		treeToNum(root.right_child,lst)


#check if value of the variables are equal with k or not
def isEqual(dict_val,var,k,eq):
	#pass
	dict_val1 = dict(dict_val)
	for i in var:
		c = dict_val[i]
		dict_val1[i] = makeS(c)
	eq = replaceVarWithVal(dict_val1,var,eq)
	root = evaluateExp(eq)
	lst = []
	treeToNum(root,lst)
	r = lst.count('s')
	if(r==k):
		return True
	else:
		return False



#checks for solution and prints the solution
def checkSolution(dict_val,var,k,p,eq):
	x = var[p]
	q = p+1
	for i in range(k+1):
		dict_val[x] = i
		if q<len(var):
			checkSolution(dict_val,var,k,q,eq)
		else:
			b = isEqual(dict_val,var,k,eq)
			if b:
				printSolution(dict_val,var)



#get all the variables from a string and return a list
def getVariables(eq):
	var = []
	for i in eq:
		if(i.isalpha()):
			var.append(i)
	return var


#make dictionary of variables and values and initialize it with 0
def makeDict(var):
	dict_val = {}
	for i in var:
		dict_val[i] = 0
	return dict_val


#convert s(s(...(0))) to a number
def makeNum(const):
	c = const.count('s')
	return c


def isConst(const):
	#print(const)
	for i in const:
		if(i=='s' or i=='0' or i=='(' or i==')'):
			pass
		else:
			return False
	return True


#main_prog

file = open("input.txt","r")
inp_eq = file.read() 

terms = inp_eq.split(" ")
eq = terms[0]
const = terms[2]
#print(isConst(const))
if eq.count('s')==0 and isConst(const):
	var = getVariables(eq)
	dict_val = makeDict(var)
	k = makeNum(const)
	p = 0
	print("######### Answers #########")
	checkSolution(dict_val,var,k,p,eq)
else:
	print("Wrong equation")
