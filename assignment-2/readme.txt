File 1 contains the program for following rules:

+(0,x) -> x
+(s(x),y) -> s(+(x,y))
*(0,x) -> 0
*(s(x),y) -> +(y,*(x,y))
fact(0) -> s(0)
fact(s(x)) -> *(s(x),fact(x)) 

Sample Input: +(x,y) = s(s(s(s(0))))

Sample Output:

######### Answers #########
-----------------
x  =  0
y  =  s(s(s(s(0))))
-----------------
-----------------
x  =  s(0)
y  =  s(s(s(0)))
-----------------
-----------------
x  =  s(s(0))
y  =  s(s(0))
-----------------
-----------------
x  =  s(s(s(0)))
y  =  s(0)
-----------------
-----------------
x  =  s(s(s(s(0))))
y  =  0
-----------------


File 2 contains the program for following rules:

a(n,x) -> x
a(c(x,y),z) -> c(x,a(y,z))
r(n) -> n
r(c(x,y)) -> a(r(y),c(x,n))

Sample Input- 

Enter LHS : r(c(x,c(y,r(c(u,c(v,n))))))
Enter RHS  : c(3,c(4,c(2,c(1,n))))

Sample output-
################# ANSWER ##################
u  =  3
v  =  4
y  =  2
x  =  1 


