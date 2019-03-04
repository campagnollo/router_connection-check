import sys, subprocess
import paramiko
import socket
from time import sleep

def show(remote, command):

    stdin, stdout, stderr=remote.exec_command(command)
    result = stdout.read()
    print(result[269:]+"\n") #print the output sans banner



def main(router):
    user="***"
    password="***"
    commands=("sh ver | i uptime","sh bgp ipv4 uni sum | b Neighbor","sh bgp ipv6 uni sum | b Neighbor")
    try:
       ip=socket.gethostbyname(router[1]) #ID device name or pass IP address
    except socket.gaierror:
       print("Device not identified on DNS")
       exit()
    print("\r") #White space
    for i in range (0,3):
       remote = paramiko.SSHClient()
       remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       try:
          remote.connect(hostname=ip, port=22,username=user,password=password, timeout=10)
          remote_transport=remote.get_transport()
       except paramiko.AuthenticationException:
          print("Authentication failed")
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
