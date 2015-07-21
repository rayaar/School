import math
def main():
	x=int(raw_input("give x: "))
	y=int(raw_input("give y: "))
	
	if x > 0 and y >0:
		a = max(x,y)
		b = min(x,y)
		print euclid(a,b)
	
def euclid(x,y):
	if y ==0:
		return x
	else:
		return euclid(y, x % y)

main()
