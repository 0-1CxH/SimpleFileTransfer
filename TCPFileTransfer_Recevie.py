#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import json
import hashlib
import progressbar, time
import sys


# In[2]:


def print_head(head):
    print("File name:",head['fname'])
    print("File size:",head['fsize'])
    print("Hash value",head['hash'])    


# In[3]:


def hash_file(filename):
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as fh:
        while True:
            data = fh.read(1024)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


# In[ ]:


arginput = sys.argv
#arginput = ['r','9777']

#usage run.py newfilename port


if(len(arginput)==2):
    port = int(arginput[1])
else :
    port = 9753
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.bind(("",port))
main_socket.listen(5)

while True:
    recv_file_sock, recv_file_addr = main_socket.accept()
    head = recv_file_sock.recv(256)
    head = json.loads(head)
    print_head(head)
    recv_file_sock.send("Confirmed".encode(encoding='UTF-8'))
    newfilename = input("Save as:")
    f = open(newfilename,"wb")
    sizecnt = 0
    
    pgbar = progressbar.ProgressBar(widgets=[progressbar.Bar(),progressbar.Percentage(),
    ' (', progressbar.SimpleProgress(), ') ',],max_value=head['block'])
    #pgbar.start()
    
    for i in range(head['block']):
        content = recv_file_sock.recv(4096)
        f.write(content)
        time.sleep(0.000000001)
        pgbar.update(i)
        
        
        sizecnt += len(content)
    f.close()
    
    if(sizecnt == head['fsize'] and hash_file(newfilename)==head['hash']):
        print("Hash verified ", head['hash'])
        print("File saved as: ",newfilename)
    
    recv_file_sock.close()


# In[ ]:


recv_file_sock.close()


# In[ ]:




