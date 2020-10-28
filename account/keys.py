import os
import random
from cryptography.fernet import Fernet
from stegano import lsb
from base64 import b64decode, b64encode
from random import randint
from secry.settings import *
import requests
import urllib.request
from django.core.files.storage import FileSystemStorage


def enc_order():        #Create crypto algorithm ordering
    order = random.sample(range(0, 3), 3)
    return order

def generateKey(id):                    #Generate the key file
    listDir = os.listdir(MEDIA_ROOT+'/keys/')
    for file in listDir:
        if file:
            file_path = os.remove(MEDIA_ROOT+'/keys/'+file)
    key = os.urandom(16)
    iv1 = os.urandom(16)
    iv2 = os.urandom(8)
    key_data = b64encode(key).decode('utf-8')
    iv1_data = b64encode(iv1).decode('utf-8')
    iv2_data = b64encode(iv2).decode('utf-8')
    data = key_data + '-' + iv1_data + '-' + iv2_data
    ipath = 'https://source.unsplash.com/random/200x200'
    fname = id + '.png'
    path = os.path.join(MEDIA_ROOT,'keys',fname)
    r = requests.get(ipath, allow_redirects=True)
    open(path, 'wb').write(r.content)
    secret = lsb.hide(path, data)             # Stegano library hiding the data
    secret.save(path)
    return key, iv1, iv2,data


def keygenerate(data, id):                              #Regenerate the key file on user request
    ipath = 'https://source.unsplash.com/random/200x200'
    fname = id + '.png'
    path = os.path.join(MEDIA_ROOT+'/keys/', fname)
    r = requests.get(ipath, allow_redirects=True)
    open(path, 'wb').write(r.content)
    secret = lsb.hide(path, data)       # Stegano library hiding the data
    secret.save(path)

def FetchKey(keyfile):                  #Fetch key file from the file.
    fs = FileSystemStorage()
    fs.save(keyfile.name,keyfile)
    path = os.path.join(MEDIA_ROOT, keyfile.name)
    data = lsb.reveal(path)       # Stegano library revealing the data
    iv = data.split('-')
    key = b64decode(iv[0].encode('utf-8'))
    iv1 = b64decode(iv[1].encode('utf-8'))
    iv2 = b64decode(iv[2].encode('utf-8'))
    os.remove(path)
    return data, key, iv1, iv2


def FetchKeyData(keyfile):  # Fetch key data file from the file.
    fs = FileSystemStorage()
    fs.save(keyfile.name, keyfile)
    path = os.path.join(MEDIA_ROOT, keyfile.name)
    data = lsb.reveal(path)
    os.remove(path)
    return data
