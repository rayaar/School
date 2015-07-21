#!/usr/bin/python
 

import subprocess 
import sys
from multiprocessing import Process, Manager
import time
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
import os

def passw(passwd,return_list,headerfile):
	try:
		luks_file = headerfile
		FNULL = open(os.devnull, 'w')
		#print 'Trying %s...' % repr(passwd)
		r = subprocess.Popen('echo %s | cryptsetup luksOpen --test-passphrase %s ' % (passwd, luks_file), 
					shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
		out, err = r.communicate()

		if len(err) == 0:
			return_list[0]="true"
			return_list[1]=repr(passwd)
		return
	except:
		sys.exit(1)



def main(headerfile,uni):
	uni = open(uni,"r")
	headerfile = headerfile
	words = []
	
	chars = set('\\ \'\"><\;|$,\`[](){}_*\t=:& #')
	jobs=[]
	luks_file = "header2"
	manager = Manager()
	return_list = manager.list(range(2))
	
	for lines in uni:
		lines = lines.strip()
		if any((c in chars) for c in lines):
			continue
		if len(lines)< 20 and len(lines)> 6 :
			words.append(lines)
	print "trying ",len(words), "potential passwords"
	words.reverse()
	nowtime =time.time()
	widgets = ['Cracking LUKS-header: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ']
	pbar = ProgressBar(widgets=widgets, maxval=len(words)).start()
	for i,passwd in enumerate(words):
		pbar.update(i+1)
		passwd = passwd.strip()
		if any((c in chars) for c in passwd):
			continue
		else:
			t =  Process(target=passw, args = (passwd,return_list,headerfile,))
			t.daemon = True
			jobs.append(t)
			t.start()
			time.sleep(.1)
		if len(jobs) >= 15:
			for j in jobs:
				j.join()
				jobs=[]
		if "true" in return_list:
			i = len(words)
			pbar.update(i)
			break
	if "true" not in return_list:
		print "No password found"
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

