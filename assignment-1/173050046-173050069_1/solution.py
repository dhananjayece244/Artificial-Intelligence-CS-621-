#!/usr/bin/python3
import sys
import string

#predefined operators, values and variables
operator = ['+','*','f']
value = ['s','0']
variable = ['x','y']
l = 99999999
ptr = None

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
def processRules():
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
		#prev_ptr.left_child = rhs[index]
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

#MAIN_PROG
sys.setrecursionlimit(10000)
content = openFile()
rhs,lhs = processRules()  #take each rule and divide it into two parts, lhs and rhs
inp_term = input("Enter Term: ") #take input
inp_term = inp_term.replace("fact","f")
print(inp_term)
root = Term(inp_term) #convert the input term into tree
replace_tree(root)
print("################# ANSWER ##################")
if(root):
	treePrint(1,root) #print final tree
else:
	print("Wrong input given.")