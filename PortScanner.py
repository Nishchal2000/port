#!/usr/bin/env python3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
  

import socket 
import threading
import concurrent.futures
import sys


def scan(ip,port,protocol,l):
    if protocol=='tcp':
    	scanner=socket.socket(socket.AF_INET,socket.SOCK_STREAM)			#Creating a socket instance, SOCK_STREAM is for TCP connections
    else:
        scanner=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)				#Creating a socket instance, SOCK_DGRAM is for UDP connections
        
    scanner.settimeout(1)		#Setting the timeout to 1 second
    try:
        result=scanner.connect_ex((ip,port))		#Connecting to the specified IP and port using the above instance created
        status='OPEN'
        if result!=0:
            status='CLOSED'
        
        service=socket.getservbyport(port,protocol)	#Finding the name of the service
        if service==None or service=='':
        	service='svc name unavailable'			# If service could not be determined
        l.append([port,status,service])       
    
    except socket.gaierror:					#Handling errors (host does not exist)
    	if l[0]==0:
    		print("Host does not exist")
    	l[0]=1
    	sys.exit()
    
    except KeyboardInterrupt:					#Keyboard interrupts
        print("Program interrupted by user.")
        sys.exit()


# 4 arguments are mandatory ( <hostname> <protocol> <portlow> <porthigh> )
if len(sys.argv)!=5:
	print("usage: ./PortScanner.py <hostname> <protocol> <portlow> <porthigh>")
	sys.exit()


#Protocol can either be 'tcp' or 'udp'
if sys.argv[2] not in ['tcp','udp']:
	print("Invalid protocol:"+sys.argv[2]+".","Specify \"tcp\" or \"udp\"")
	print("usage: ./PortScanner.py <hostname> <protocol> <portlow> <porthigh>")
	sys.exit()


#Checking to see if values entered are correct
try:
	sys.argv[3]=int(sys.argv[3])
	sys.argv[4]=int(sys.argv[4])

except:
	print("usage: ./PortScanner.py <hostname> <protocol> <portlow> <porthigh>")
	sys.exit()

#Checking if the port range is correct
if sys.argv[3]<0 or sys.argv[4]>65535 or sys.argv[3]>sys.argv[4]:
	print("usage: ./PortScanner.py <hostname> <protocol> <portlow> <porthigh>")
	sys.exit()



l=[0]
port_low=sys.argv[3]
port_high=sys.argv[4]

print("Scanning host =",sys.argv[1]+",","protocol =",sys.argv[2]+",","ports:",str(sys.argv[3])+"->"+str(sys.argv[4])+'\n')

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:		#Executing the tasks in parallel to speed up the process
	for port in range(port_low,port_high+1):
		executor.submit(scan,sys.argv[1],port,sys.argv[2],l)

l=sorted(l[1:], key=lambda x: x[0])
for port in l:
	color =  bcolors.OKGREEN if port[1] == "OPEN" else ''
	endcolor = bcolors.ENDC if port[1] == "OPEN" else ''
	if port[2]!='svc name unavailable':
		#Printing the output (open ports highlighted in green) (printing only those ports whose service could be determined)
		print( "{4}Port {0}:      Status:{2}      Protocol:{3}    Service:[{1}]{5}".format(port[0], port[2], port[1], sys.argv[2], color, endcolor))
