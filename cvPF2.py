#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# This example formulates and solves the following simple MIP model:
#  maximize
#        w1*b1 + w2*b2 +w3*b3 = > log (b1*b2*b3)
#  subject to
#         b_j = r_ij*p_ij
#         p11+p12+p13<=1
#         p11+p21<=1
#  x, y, z binary
"""
if __name__ =="__main__":

  
    m = Model("cvPF")
    # The number of users
    U = 3
    
    #The number of APs
    A = 2
    # The rate matrix
    
    r = [[6.0, 48.0, 32.0],
         [0.0, 12.0, 6.0]]

    # The weight (priority) of users
    w = [1.0, 1.0, 1.0]
    # The alpfa
    a =1 + math.sqrt(2)
    cvPF(U,A,r,w,a)
"""
from gurobipy import *
from rounding import *
from wireless_80211b import *
from matplotlib import *
import math

def f(u):
    return math.log(u)

def find(xi):
    total_x = 0
    for xij in xi:
        total_x = total_x + xij
        if total_x >= 1:
            t_x = 0
            print(total_x)
           # for j in range(len(total_x)-1):
             #   x2i.append(total_x(j))
            #    t_x = t_x + total_x(j)
           # x2i.append(1-t_x)


def cvp(model,U,A,r,w):
    """
     # This example formulates and solves the following simple MIP model:
     #  maximize
     #        w1*b1 + w2*b2 +w3*b3 = > log (b1*b2*b3)
     #  subject to
     #         b_j = r_ij*p_ij
     #         p11+p12+p13<=1 ...
     #         p11+p21<=1  ...
    """
    p = []
    b = []

    for i in range(A):
        p.append([])
        for j in range(U):
            p[i].append (m.addVar(lb = 0, ub = 1,name = 'p')) 
    
    
    for j in range(U):
        b.append(m.addVar(name = 'b'))
 
    # Add constraint
   
    for j in range(U):
        m.addConstr(quicksum(r[i][j]*p[i][j] for i in range(A))== b[j],'c0')
    for i in range(A):
        m.addConstr( quicksum(p[i][j] for j in range(U)) <= 1, 'c1')
    for j in range(U):
        m.addConstr(quicksum(p[i][j] for i in range(A)) <= 1, 'c2')

    # Add piecewise-linear objective functions

    lb = 0.1
    ub = 100
    npts = 1000
    ptu = []
    ptf = []

    for j in range(npts):
       ptu.append(lb + (ub - lb) * j/ (npts))
       ptf.append(f(ptu[j]))
       #print(lb + (ub - lb) * j/ (npts - 1))
    for j in range(U):
       m.setPWLObj(b[j], ptu, ptf)
    
    m.ModelSense = GRB.MAXIMIZE
   

    
  #  m.setObjective(sum(b[j] for j in range(U)), GRB.MAXIMIZE)

    m.optimize()

   # for v in m.getVars():
        #print('%s %g' % (v.varName, v.x))

    #print('Obj: %g' % m.objVal)
    return p,b



       
def cvPF(U,A,r,w,a):
    # Create a new model
    """
       solve the cvp
    """
    p,c = cvp(m,U,A,r,w)
    #print ("##############Solve the convex problem#############")
    """
    rounding process which is exceed via bipartite min-cost flow
    1) Obtain the stronge edages as p1 and delete the weak edages (e.g. (2,2))
    """
   
    p1 = []
    x = []
    for i in range(A):
       p11 = []
       for j in range(U):
          # print(a*r[i][j])
          # print(c[j].x)
         #  print a
           if c[j].x != 0:
               x.append( p[i][j].x*r[i][j]/c[j].x )
           else:
               x.append(0)
           if c[j].x > a*r[i][j]:
              p11.append(0)
           else:
              p11.append(p[i][j].x)
       p1.append(p11) 
    print("#############   step1 - x    #########")
    #print (x)
    print("#############   step2 - strong p'     ###############")
   # print(p1)
    #2) assignment the factor
    
  
    b1 = []
    x1 = []
    q1 = []


    for j in range(U):
        b1.append(sum(r[i][j]*p1[i][j] for i in range(A)))

    for i in range(A):
       x11 = []
       q11 = []
       for j in range(U):
           if c[j].x != 0:
               x11.append((r[i][j]*p1[i][j])/b1[j])
           else:
               x11.append(0)           
           if r[i][j] != 0:
               q11.append(b1[j]/r[i][j])
           else:
               q11.append(0)
       x1.append(x11)
       q1.append(q11)
    print("step2 - bj")
    #print(b1)
    print("step2 -  q")
    #print(q1)#this is the cost of x2 in  step 4
    print("step2 - x' ")
    #print(x1)#this is the cost of x2 in  step 4

    """
       Set up the GAP using (x1 and q1)
    """ 

   
    
    #Construct the bipartite graph and utility
    uti = []
    for i in range(A):
        utility = []
        for j in range(U):
            if r[i][j]*p1[i][j] != 0:
                utility.append(f(r[i][j]*p1[i][j]))
            else:
                utility.append(0)
        uti.append(utility)
    print("The utility of users")
    #print(uti)
   
    

    print("################ step3 - After the first step of rounding ##################")
    x2,utility2,assign = rounding(x1,uti)
   # print(x2)
    """
       The Hungarian Algorithm 
       1. set the cost value 
       2. call the hungarian algorithm  to otain the assignment of AP and Users
    """
    """
    for xj in x2:
        print(xj)
       # print(len(xj))
    print("The length of x' is %d " % len(x2))
    for cj in utility2 :
       print cj
      # print len(cj)
    print("The length of c' is %d " % len(utility2 ))
   # hungarian(utility2 )
    """
    print("step4 - (x,y) is the assignmnet of association which AP x is assignment to user y")
    #for ass in assign:
       # print ass
    
    x3 = []# the matrix style of assignment
    for  i in range(A):
        x33=[]
        for j in range(U):
              t = (i,j)
              if t in assign:
                  x33.append(1)
              else:
                  x33.append(0)
        x3.append(x33)
    print("The form of the matrix of the assignment")
    #print x3 
 
   
        
    """
        3. reassign the value of thr bandwidth and time 

    """
    print("############   step4-the final result   ##########")
    p2 = []# the value of P^ in paper
    for i in range(A):
       p22 = []
       for j in range(U):
              if r[i][j]!=0:
                  p22.append(x3[i][j]*b1[j]/((1+a)*r[i][j]))
              else:
                  p22.append(0)
       p2.append(p22) 
    print("step4 -  p(time)")
    #print p2

    b2=[]
    for j in range(U):
        b2.append(sum(r[i][j]*p2[i][j] for i in range(A)))
    
    print("step4 - bj(bandwidth)")
    #print(b2)
    print("##################################")
    return b2

# This is the main function which contains two approximate algorithm:cvapPF and nlapPF
# The sub_function is:
#               scenario function
#               cvapPF
#               nlapPF

if __name__ =="__main__":
    A = 20 # The number of APs
    U = 250 # The number of Users
    distance = 100 # The distance between the adjacent APs
    coverage = 150
    w = [1.0]*U
    a =1 + math.sqrt(2)
    m = Model("cvPF")
    User_x = []
    User_y = []
    userb = []# this is to construct the mid matrix of bandwidth
    t = 100#rerun time
    #### circle 100 times to obtain the average value#########
    for k in range(t):
        rate = scence(A,U,distance,coverage)
        b = cvPF(U,A,rate,w,a)
        #b.sort()
        #print("######### The bandwidth of each user  ###########")
        User_bx = []
        User_by = []
        for j in range(100):
            User_by.append(b[j])
        userb.append(User_by)
    #print User_bx
    #print rate
    #plt.plot(AP_x,AP_y,'ro')
      print("Round Times %d"%k)
    print len(userb)
    for  i in range(100):
        User_x.append(i)
    by1 = map(sum,zip(*userb))
    for j in by1:
        User_y.append(j/t)
    User_y.sort()
    plt.plot(User_x,User_y,'.')
    plt.show()
    
