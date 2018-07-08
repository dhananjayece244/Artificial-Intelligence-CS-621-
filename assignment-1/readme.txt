173050046-173050069_1 contains the program for following rules:

+(0,x) -> x
+(s(x),y) -> s(+(x,y))
*(0,x) -> 0
*(s(x),y) -> +(y,*(x,y))
fact(0) -> s(0)
fact(s(x)) -> *(s(x),fact(x)) 

Sample Input: +(s(s(0)),s(0))

Sample Output:

################# ANSWER ##################
1   s
2   s
3   s
4   0


173050046-173050069_2 contains the program for following rules:

a(n,x) -> x
a(c(x,y),z) -> c(x,a(y,z))
r(n) -> n
r(c(x,y)) -> a(r(y),c(x,n))

Sample Input: r(r(c(1,c(2,c(3,n)))))

Sample Output: 

################# ANSWER ##################
c
1
c
2
c
3
n

