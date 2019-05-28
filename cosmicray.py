# need to sort: 
#    define file path so program can be run from any location?
#    A better way of selecting files that need processed
#    Quantitative method for deciding on optimal settings

import os, shutil, glob, time
from os.path import exists

## checking for login.CL file, need to be in place before IRAF can run
if exists('login.cl') is False:
        print "creating CL file"
        shutil.copy('/Users/cgibson/login.cl',os.getcwd())
        time.sleep(1)
else:
	print "login.CL file already exists"

## initialising PYRAF and STSDAS    
from pyraf import iraf 
#iraf.noao()
iraf.stsdas()

## Checking for LACOS temp files, if these exist the program would crash	
delLACOS = 0
inLACOS = list(glob.glob(os.path.join('LACOS*.*')))
if not inLACOS:
    print 'No LACOS files, continuing:'
else:
    delLACOS = raw_input('LACOS temp files exist, delete these before proceeding? (y/n)')
if delLACOS == 'y':
    print "removing LACOS files"
    for f in inLACOS:
        os.remove(f)

#Produce input and output file names (Need to fix for file duplicates)
inlist = list(glob.glob(os.path.join('wi*.*')))
outlist = ["c" + file for file in inlist]
i = len(inlist)

## checking if output files already exist, if they do program would crash
outfile='false'
outdel=[]
delC = []
for f in outlist:
    if exists(f) is True:
        outfile = 'true'
        outdel.append(f)
        
if outfile == 'true':        
    delC = raw_input('Output files exist, delete these and proceed (y/n)?')
    
if delC == 'y':
    		print "removing old output files"
    		for f in outdel:
        		os.remove(f)
        	outfile = 'false'
if delC == 'n':
	print "Exiting!! CANT process files while output files already exist, delete these then re-run"        

## starting to process files
if outfile == 'false':
	print "Files to process: ", i 

	##EPAR settings for LACOS.SPEC
	iraf.lacos_spec.gain = 1.2
	iraf.lacos_spec.readn = 4.2
	iraf.lacos_spec.xorder = 3.0
	iraf.lacos_spec.yorder = 3.0
	iraf.lacos_spec.sigclip = 3.9
	iraf.lacos_spec.sigfrac = 2.0
	iraf.lacos_spec.objlim = 1.0
	iraf.lacos_spec.niter = 4
	iraf.lacos_spec.verbose = "n"
		
	#processing LACOS on each file
	start = time.time()
	n=0
	while n < i:
  		print "workin on file", inlist[n], "(", n+1, ")"
  		iraf.lacos_spec(inlist[n], outlist[n], 'temp.pl')
  		n +=1
  		os.remove('temp.pl')
  		time.sleep(5) #Needed as LACOS was slow at deleting LACOS files when it finishes
       
	end = time.time()
	print "Run Time: ", end - start
		
print 'Program finished'