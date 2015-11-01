#!/usr/bin/python
 

import subprocess 
import sys
from multiprocessing import Process, Manager
import time
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage,ProgressBar, ReverseBar, RotatingMarker,SimpleProgress, Timer
import os
import commands
import re



def passw(passwd,return_list,headerfile):
	try:
		luks_file = headerfile
		#print 'Trying %s...' % repr(passwd)
		st = "cryptsetup luksOpen --test-passphrase "+passwd + " "  + luks_file
		r = subprocess.Popen('echo %s | cryptsetup luksOpen --test-passphrase %s ' % (passwd, luks_file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	        out, err = r.communicate()
		if len(err) == 0:
			return_list[0]="true"
			return_list[1]=repr(passwd)
		return []
	except:
		sys.exit(1)



def main(headerfile,uni):
	uni = open(uni,"r")
	headerfile = headerfile
	words = []
	
	jobs=[]
	luks_file = uni
	manager = Manager()
	return_list = manager.list(range(2))
	for lines in uni:
		lines = lines.strip()
		pattern = r'[^\.\w\!]'
		sa = re.search('[^\.\w\!]', lines)
		if not sa and len(lines) > 2:
			words.append(lines)
	print "trying ",len(words), "potential passwords"
	words.reverse()
	nowtime = time.time()
	widgets = ['Cracking LUKS-header: ', Percentage(), ' ', Bar(marker="|"), ' ', ETA(),]
	pbar = ProgressBar(widgets=widgets, maxval=len(words)).start()
	for i,passwd in enumerate(words):
		pbar.update(i+1)
		t =  Process(target=passw, args = (passwd,return_list,headerfile,))
		jobs.append(t)
		if len(jobs) == 10 or (i == len(words)-1):
		    for job in jobs:
                        job.start()

		if (len(jobs) == 10) or (i == len(words)-1):
		    #print "merge"
		    for job in jobs:
		        job.join()
		        jobs=[]

		if "true" in return_list:
			i = len(words)
			pbar.update(i)
			break
	pbar.finish()
	
	print  "time used: ", (time.time() - nowtime) / 60,"Min"
	if "true" not in return_list:
		print "No password found"
	else:
		print "password is ",return_list[1]
    	return 0

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.stderr.write("Need a headerfile \n")
		sys.exit(1)
	headerfile = sys.argv[1]
	if len(sys.argv) < 3:
		sys.stderr.write("Need a file containing potential passwords \n")
		sys.exit(1)
	uni = sys.argv[2]
	try:
		main(headerfile,uni)
	except KeyboardInterrupt:
		print "############   got controll + c, exiting   ############"
		sys.exit(1)

