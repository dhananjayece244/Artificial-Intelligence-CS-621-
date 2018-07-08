#!/usr/bin/python3
import sys
import string

#predefined operators, values and variables
operator = ['a','r']
value = ['c','n']
variable = ['x','y','z']
l = 99999999
ptr = None
lst = []

class Term(object):
	term_value = None
	left_child = None
	right_child = None
	def __init__(self,string):
		self.term_value = string[0]
		x = string[0]
		#for + and *
		if(x=='a'):
			k = findComma(string)
			left = string[2:k]
			right = string[k+1:-1]
			self.left_child = Term(left)
			self.right_child = Term(right)
		#for f
		elif(x=='r'):
			left = string[2:-1]
			self.left_child = Term(left)
			self.right_child = None
		#for s
		elif(x=='c'):
			v = findComma(string)
			#print(v)
			v = int(v)
			left = string[2:v]
			right = string[v+1:-1]
			self.left_child = Term(left)
			self.right_child = Term(right)
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
	            fout.write(line)
	#read the rules file
	with open("new_rules.txt") as f:
	    content = f.readlines()
	content = [x.strip() for x in content]
	return content 

#removes implies and make each rule a tree

def processRules():
	rhs = [] 
	lhs = []
	for i in content:
		a = i.rsplit(" ",2)
		print(a)
		x = Term(a[2])
		y = Term(a[0])
		rhs.append(x)
		lhs.append(y)
	return rhs,lhs	

#prints preorder traversal of the tree
def treePrint(root):
	if root:
		print(root.term_value)
		treePrint(root.left_child)
		treePrint(root.right_child)

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
def findRule(subtree_ptr):
	
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
def applyRule(subtree,index):
	#start
	if(index==0):
		x=subtree.right_child
		subtree.term_value = x.term_value
		subtree.left_child = x.left_child
		subtree.right_child = x.right_child
	elif(index==1):
		x = subtree.left_child.left_child
		y = subtree.left_child.right_child
		z = subtree.right_child
		temp=Term("0")
		temp.term_value=subtree.term_value
		subtree.term_value = subtree.left_child.term_value
		temp.left_child = y
		temp.right_child = z
		subtree.right_child = temp
		subtree.left_child = x

	elif(index==2):
		subtree.term_value='n'
		subtree.left_child=None
		subtree.right_child=None
		#prev_ptr.left_child = rhs[index]
	elif(index==3):
		x = subtree.left_child.left_child
		y = subtree.left_child.right_child
		c = subtree.left_child
		

		temp=Term("0")
		temp.term_value = subtree.term_value
		temp.left_child = y

		temp1 = Term("0")
		temp1.term_value = 'c'
		temp1.left_child = x
		temp1.right_child = Term("n")

		subtree.term_value = 'a'
		subtree.right_child = temp1
		subtree.left_child = temp
	if isOperatorPresent(subtree):
		replace_tree(subtree)

#replace subtree with new subtree formed by unification using rules and return the root of the tree
def replaceSubtree(subtree_ptr):
	#start
	index = findRule(subtree_ptr) #find the rule that to be applied on the subtree
	if(index!=-1):
		applyRule(subtree_ptr,index) #apply the rule and do the unification

def replace_tree(root):
	if root:
		replace_tree(root.left_child)
		replace_tree(root.right_child)
		if root.term_value in operator:
			replaceSubtree(root)

def match_and_assign(root,root_r):
	if(root and root_r):
		if(root.term_value !=root_r.term_value):
			print(root.term_value, " = ", root_r.term_value)
		match_and_assign(root.left_child,root_r.left_child)
		match_and_assign(root.right_child,root_r.right_child)

#MAIN_PROG
sys.setrecursionlimit(10000)
content = openFile()
rhs,lhs = processRules()  #take each rule and divide it into two parts, lhs and rhs

print("-----------------------------")
inp_term = input("Enter LHS : ") #take input
inp_term = inp_term.replace("app","a")
inp_term = inp_term.replace("rev","r")

root = Term(inp_term) #convert the input term into tree
#treePrint(1,root)
replace_tree(root)
out_term = input("Enter RHS  : ") #take input
out_term = out_term.replace("app","a")
out_term = out_term.replace("rev","r")

root_r = Term(out_term) #convert the input term into tree
print("################# ANSWER ##################")
match_and_assign(root,root_r)
