#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# The rounding process via the general assignment problem

from gurobipy import *
import math
from munkres import Munkres, print_matrix
import sys

def find_j1(xi):
    total = 0
    for j in range(len(xi)):
          total +=  xi[j]
          if total >=1:
             return j
             break

def find_js(xi,s):
    total = 0
    for j in range(len(xi)):
          total +=  xi[j]
          if total >=s:
             return j
             break
def create_xv1(xi,j1,x_vi1,x_vi2):
    total = 0
    for j in range(j1):#notice the index is from 0
        if xi[j] > 0:
            x_vi1.append(xi[j])
            total += xi[j]
        else:
            x_vi1.append(0)
        x_vi2.append(0)
    x_vi1.append(1-total)
    total += xi[j1]#xu hao cong 0 kai shi
            #print total
    if total >1:
        x_vi2.append(total -1)
    else:
        x_vi2.append(0)  
                 #print(x_vi2)
    return x_vi1,x_vi2 

def create_xvs(s,j_s_1,js,xi,x_vs,x_vs1):
    total = 0
    #print(j_s_1)
    #assign the point in (vs,w_{js-1})
    for xij in xi[j_s_1 + 1:js]:#notice the index is from 0
       # print xij
        if xij > 0:
            x_vs.append(xij)
        else:
            x_vs.append(0)
    #x_vs1.append(0)
    total = sum(x_vs)
    #print total
    x_vs.append(1-total)
    total1 = sum(xi[0:js+1])#xu hao cong 0 kai shi
    #print total1
    for j in range(js):
        x_vs1.append(0) 
    if total1 > s: 
        x_vs1.append(total1 - s)
    else:
        x_vs1.append(0) 
    #print(x_vs1)
    return x_vs,x_vs1 
def cost(x,xi,x_vi1,c):
    i = x.index(xi)
    c22 = []
    for ci in x_vi1:
            j1 =  x_vi1.index(ci)
            if ci !=0:
                c22.append(c[i][j1])
            else:
                c22.append(0)
    return c22

def rounding (x,c):

    x2 = []
    c2 = []
    k = [0]
    t = 0
    for xi in x:
        x22 = [] 
        x_vi1 = []
        x_vi2 = []
        x_vsi1 = []
        ki = int(math.ceil(sum(xi)))
        t +=ki
        k.append(t)
        #print(ki)
        if sum(xi) <=1:
             for  xij in xi:
                if xij>0:
                    x_vi1.append(xij)
                else:
                    x_vi1.append(0)
        else:
             j1 = find_j1(xi)
             x_vi1,x_vi2 = create_xv1(xi,j1,x_vi1,x_vi2)
             for j in range(j1+1,len(xi)):
                 #print j
                 x_vi1.append(0)
             j_s_1 = j1
             x_vs = x_vi2
             #print x_vi2
             for s in range(2, ki):#shu chu wei 2
                x_vs1 = []
                #print s 
                js = find_js(xi,s) 
                #print js #the index from 0
                x_vs,x_vs1 = create_xvs(s,j_s_1,js,xi,x_vs,x_vs1) 
                j_s_1 = js
                for j in range(js+1,len(xi)):
                    x_vs.append(0)
                x22.append(x_vs)
                x_vs = x_vs1
                j_last = js
                
             #print j_last
             x_vsi1 = x_vs1
             for xij in xi[j_last+1:len(xi)]:
                 if xij >0:
                     x_vsi1.append(xij)
                 else:
                     x_vsi1.append(0)
        x2.append(x_vi1)# v_{i1} is the first virtual node of node i
        c2.append(cost(x,xi,x_vi1,c))
        for xj in x22:
            x2.append(xj)# x22 is the 2,...ki-1 virtual node of node i
            c2.append(cost(x,xi,xj,c))
        if x_vsi1 !=[]:
            x2.append(x_vsi1)# x_vsi1 is the ki virtual node of node i
            c2.append(cost(x,xi,x_vsi1,c)) 
    print("######The Result of Max-coat ALgorithm#######") 
    indexes1,total =  hungarian(c2)
   #print indexes1
    #print k
    assign = []
    for row, column in indexes1:
        value = c2[row][column]
        for i in range(len(k)):
            if (row >=k[i]) and (row <k[i+1]):
                 #print '(%d, %d)->%f' %(i, column,value)
                 assign.append((i, column))
        #print column
    print assign

    print 'total profit=%f' % total#the matrix is the cost
    #print("###########################################")  
    return x2,c2,assign

def hungarian(matrix):
    """
    matrix = [[5, 9, 1],
          [10, 3, 2],
          [8, 7, 4]]
    """
    
    cost_matrix = []
    for row in matrix:
       cost_row = []
       for col in row:
          cost_row += [sys.maxint - col]
       cost_matrix += [cost_row]

    m = Munkres()
    indexes = m.compute(cost_matrix)
    #print_matrix(matrix, msg='Maximum cost through this matrix:')
    
    total = 0
    for row, column in indexes:
       value = matrix[row][column]
       total += value
      # print '(%d, %d) -> %f' % (row, column, value)
   
    return indexes,total

if __name__ =="__main__":
    x1 = [[1.0/3,1,1,0,0,0,0],
          [1.0/3,0,0,1,1,0,0],
          [1.0/3,0,0,0,0,1,1]]
    c1 = [[3.2,0.9,1,1,1,1,1],
          [3,1,1,1,1,1,1],
          [3,1,1,1,1,1,1]]
    #"""
    #x1 = [[1.0,1.0,0.24],[0.0, 0.0, 0.9753199868723336]]
    x3,c2,assign = rounding(x1,c1)#It is the x' in rounding
    """
    for xj in x3:
        print(xj)
        print(len(xj))
    print("The length of x' is %d " % len(x3))
    for cj in c2:
       print cj
       #print len(cj)
    print("The length of c' is %d " % len(c2))
    """
