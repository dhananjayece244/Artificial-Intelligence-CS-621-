Team details:

Team name: DD
Roll- 173050069
	  173050046

Commands to run the code:
	
	Open this folder in terminal.
	Run - python3 solution.py
	
	Enter the term to be normalized, e.g- *(f(s(s(0))),*(s(s(0)),s(s(0)))) 
Description of code:
 Step-1: 

 Reading rules.txt file line by line and converting the rules in string formate into two tree structure. One is for left side of rule and another for right side of rule. And storing the root node of each left root and right root of rules in list lhs[] and rhs[] respectively.

 Step-2: 
 Taking input term to be solved as input from user. Note that input term should be in correct formate as given in the rules.
 
 Step-3:
 Converting input term in string formate into tree structure. 

 step-4: After getting the tree from step-3, it will go for parsing and unification. Now, tree will be travered in post-order traversal and will check for operator at each node. If value at current node is an operator then it checks for the rules to be applied for this particular operator. After getting rule number to be applied, it does unification according to the rules. After unifying current operator, it again checks for operator present in this current subtree after unification. If it contains any operator then again this subtree would be send for parsing and unification in that post-order parsing method.

 step-5: After complete unification(when tree is free from operators), it prints the unified tree and that is the normalized form of input term.
Assumptions-

1. Input terms should be in correct format. For example, Unary operator should contain exactly one
   term and binary operator should have exactly two terms which should be separated by comma. 
