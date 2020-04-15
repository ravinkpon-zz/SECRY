from django.core.files.storage import FileSystemStorage
from fsplit.filesplit import FileSplit
from django.shortcuts import render
from django.http import request
from .encrypt import *
from .decrypt import *
from secry.settings import *
import os
readsize = 1024


def split(file):                            # File split function 
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    source = os.path.join(MEDIA_ROOT,filename)
    dest = os.path.join(MEDIA_ROOT, 'temp/')
    chunks = (int)((file.size)/3)
    fs = FileSplit(source, chunks, dest)
    fs.split()
    os.remove(source)
    fname = filename.split('.')
    dest1 = dest + fname[0] +'_3.' + fname[1]
    dest2 = dest + fname[0] + '_4.' + fname[1]
    if(os.path.exists(dest1)):
        with open(dest1,'ab') as f:
            fl = open(dest2,'rb').read()
            f.write(b'\n'+fl)
        os.remove(dest2)

def join(fromdir, tofile):              # File joining function
    parts = os.listdir(fromdir)
    parts.sort()
    for filename in parts:
        output = open(tofile, 'ab')
        filepath = os.path.join(fromdir, filename)
        fileobj = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(readsize)
            if not filebytes:
                break
            output.write(filebytes)
        output.close()
        fileobj.close()
        os.remove(filepath)

def encypt(alnum, key, file_path, iv):          # Function to call encyption on generated order
    if(alnum == 0):
        AES(key, file_path, iv)
    elif(alnum == 1):
        DES(key, file_path, iv)
    elif(alnum == 2):
        RC4(key, file_path, iv)


def decrypt(alnum, key, file_path, iv):          # Function to call decyption on generated order
    if(alnum == 0):
        DAES(key, file_path, iv)
    elif(alnum == 1):
        DDES(key, file_path, iv)
    elif(alnum == 2):
        DRC4(key, file_path, iv)
