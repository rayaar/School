#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Find how many palindrome numbers between 1 and 1000000
#  palindrome number : 1001, 0000, 0110 (same number if you read left to right or right to left)


def ins(a):
	a = str(a)
	b = a[::-1]
	if a == b:
		return True
	else:
		return False
def main():
	count = 0
	for i in range(1,1000000):
		octo = oct(i)[1:]
		if ins(i) and ins(octo):
			count +=1
	print count
	return 0

if __name__ == '__main__':
	main()

