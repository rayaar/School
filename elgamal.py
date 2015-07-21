def egcd(a, b):
	""" Find GCD of A and B """
	x,y, u,v = 0,1, 1,0
	while a != 0:
		q,r = b//a,b%a; m,n = x-u*q,y-v*q
		b,a, x,y, u,v = a,r, u,v, m,n
	return b, x, y
    
def modinv(a, m):
	""" find the mode inverse of A modulo m"""
	g, x, y = egcd(a, m)	
	if g != 1:
		return None  # modular inverse does not exist
	else:
		return x % m


def main():        
	""" ElGamal cryptosystem implemented in python.
	Assumes correct input (like p is prime and so on. """
	p= int(raw_input("give a prime: "))       #29  	#prime number
	alfa=int(raw_input("give alpha: "))  		#3 		#alfa: primitive root
	a=int(raw_input("give small a: "))			#15		#the secret key
	beta =alfa**a % p	#beta: alfa raised to the power of a.
	pubkey = p, alfa, beta #the publik key
	
	print "Public key =" ,pubkey
	m=int(raw_input("give a message (integer) to be encrypted: ")) #the message to be decrypted
	print "Message to be encrypted:", m
	k= 11	# a random number
	
	r = alfa**k %p 	
	t = beta**k * m %p
	encrypted = t,r
	print "Encrypted message:" ,encrypted #the encrypted text for bob to encrypt.

	a_inv = modinv(a,p) #the modulo inverse of a module p.
	decr= (a_inv**r) *t %p  #decryption-function
	print "Decrypted message:", decr
	print "Decrypted correctly?",decr == m			#print if decrypted text is same as message sent to bob.
	
main()
"""output:

give a prime: 29
give alpha: 3
give small a: 15
Public key = (29, 3, 26)
give a message (integer) to be encrypted: 7
Message to be encrypted: 7
Encrypted message: (11, 15)
Decrypted message: 7
Decrypted correctly? True

"""

