# This program is to generate 20 APs and 250 Users
# The data rate of each user is only related to the distance to its AP 
#    Here, we assume the distance is in [0,50] meters the data rate is 11Mbps
#    [0,50]---->11Mbps (50,80]---->5.5Mbps  (80,120]---->2Mbps (120, 150]---->1Mbps 
# The coverage of each AP is 150 meters


######## Create the 5*4 APs ##########
#AP & User's location
import math
from distance_rate import *
import numpy as np
import sys
import matplotlib.pyplot as plt
from random import randint
def f(x):
  return int((x)/5)
def g(y):
  return (y)%5

#A = 20
#U = 250
def scence(m,n,distance,coverage):
	rate =[]
	AP_x = [ f(i)*distance+distance for i in range(0,m) ]
	AP_y = [ g(i)*distance+distance  for i in range(0,m) ]
	#print(AP_x)
	#print(len(AP_x))
	#print(AP_y)
	#print(len(AP_x))
    
	User_x = [randint(1,max(AP_x)+distance) for i in range(0,n)]
	User_y = [randint(1,max(AP_y)+distance) for i in range(0,n)]
    #print(User_x)
    ###########Each AP and User's location  is set up#######
	for i in range(0, m):
		rate1 = []
		for j in  range(0, n):
			dist = ((AP_x[i]-User_x[j])**2 + +(AP_y[i]-User_y[j])**2)**0.5
			if (dist<coverage):  # The maximum transmission range is 150 meters
			 rate1.append(distance_rate(dist))
			else:
				rate1.append(0)
		#print len(rate1)
		rate.append(rate1)
	#plt.plot(AP_x,AP_y,'ro')
	#plt.plot(User_x,User_y,".")
	#plt.show()
	return rate






###############################

m = 2; # The number of APs
n = 25; # The number of Users
distance = 100 # The distance between the adjacent APs
coverage = 150
rate = scence(m,n,distance,coverage)
#print rate


         	
