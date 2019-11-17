#!/usr/bin/env python
# coding: utf-8

# In[4]:


import socket
import os
import json
import hashlib
import sys
import progressbar


# In[5]:


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





# In[7]:


arginput = sys.argv

#array = ['run','1.dmg','localhost','9777']
#arginput = array
#usage run.py filename IP port

if (len(arginput)>=3):
    if(len(arginput)==4):
        port = int(arginput[3])
    else :
        port = 9753
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.connect((arginput[2],port))
    filename = arginput[1]
    f = open(filename,"rb")
    f_size = os.path.getsize(filename)
    blockamount = int(f_size/4096)+1
    header= {
        'fname': filename,
        'fsize': f_size,
        'block': blockamount,
        'hash' : hash_file(filename)
    }
    h = json.dumps(header)
    
    main_socket.send(h.encode(encoding='UTF-8'))
    
    confm = main_socket.recv(256)
    if(confm==b"Confirmed"):
        print("Start to send file ",filename)
    main_socket.sendall(f.read())
    f.close()
    print("Finished")
    main_socket.close()
    


# In[ ]:




