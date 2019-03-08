import sys, subprocess
import paramiko
import socket
from time import sleep

def show(remote, command):

    stdin, stdout, stderr=remote.exec_command(command)
    result = stdout.read()
    i=250
    while result[i]!="U" and result[i]!="N" and result[i]!="P" and result [i]!="p":
       i+=1
    print(result[i:]+"\n") #print the output sans banner

def main(router):
    d={}
    with open("sites.txt") as site:
        for line in site:
          key, val = line.split()
          d[str(key)] = val
    if router[0]=="P" or router[0]=="p":
        user=""
        password="****"
    else:
        user="****"
        password="****"
    commands=("sh ver | i uptime","sh bgp ipv4 uni sum | b Neighbor","sh bgp ipv6 uni sum | b Neighbor")
    try:
       ip=socket.gethostbyname(router[1]) #ID device name or pass IP address
    except socket.gaierror:
       print("Device not identified on DNS")
       exit()
    try:
        if d[ip]=="True":
           for i in range (0,5):
               print("*****critical******")
    except KeyError:
       print("Device not found on critical db")
	   
    print("\r") #White space
    for i in range (0,3):
       remote = paramiko.SSHClient()
       remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       try:
          remote.connect(hostname=ip, port=22,username=user,password=password, timeout=10)
          remote_transport=remote.get_transport()
       except paramiko.AuthenticationException:
          print("Authentication failed")
          exit()
       else:
          show(remote,commands[i]) #If connected, run through 'show' commands
       remote.close()

if __name__ == '__main__':
#"""Python interpreter check"""
    try:
        assert sys.version_info[0]<3
    except AssertionError:
        print("Incorrect interpreter being run. Please use Python 2.x")
        exit()
    main(sys.argv)
