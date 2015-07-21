#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  TWThreshold.py
#  
#  Copyright 2015 raymond <raymond@aarseth.me>
#  
#  

import numpy as np
from sympy import Matrix
from random import choice

def calc_sum(A):
	rA, pivots =  Matrix(A).rref()
	col,row = rA.shape
	sm=rA[row-1]
	print 
	print rA
	return sm
	
def solve_thresh(users,p):
	arrays = []
	for items in users:
		a,b=items
		t = np.array([1,(a),(a**2),(b)])
		arrays.append(t)
	q=np.vstack(arrays)
	print q
	sm=calc_sum(q)
	return sm
	
	
	
	
def main():
	"""
	p=37
	#m=
	users=[(1,5),(2,11),(5,18)]
	print "Users: ",users
	sm=solve_thresh(users,p)
	so =sm
	print so%p
	#print m%p

	"""
	#eksempel:
	p=29
	t=3 #personer som trengs for å låse opp.
	w=6 #personer med
	s=1234 #hemmeligheten å skjule
	num1=166 #at random
	num2=94  #at random
	parts = []
	for i in range(1,w):
		num=s+num1*i+num2+i^2
		num=i,num
		parts.append(num)
	print "nøkkelpar: " 
	print parts
	
	users=[]
	while(len(users) < t):
		user = choice(parts)
		if user not in users:
			users.append(user)
	users =[parts[1],parts[3],parts[4]]
	print 
	print "solving for: "
	print users
	
	
	sm=solve_thresh(users,p)
	print sm%p
	print s%p

	return 0

if __name__ == '__main__':
	main()
