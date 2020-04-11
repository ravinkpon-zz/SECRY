from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import os


def AES(key, file_path, iv):                        # AES encryption function
    f = open(file_path, "r", encoding='utf-8')
    content = f.read()
    f.close()
    content = content.encode()
    b = len(content)
    if(b % 16 != 0):
        while(b % 16 != 0):
            content += " ".encode()
            b = len(content)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    cont = encryptor.update(content) + encryptor.finalize()
    open(file_path, "wb").close()
    f = open(file_path, "wb")
    f.write(cont)
    f.close()


def RC4(key, file_path, iv):                        # RC4 encryption function
    f = open(file_path, "r",encoding='utf-8')
    content = f.read()
    f.close()
    content = content.encode()
    b = len(content)
    if(b % 16 != 0):
        while(b % 16 != 0):
            content += " ".encode()
            b = len(content)
    backend = default_backend()
    cipher = Cipher(algorithms.ARC4(key), mode=None, backend=backend)
    encryptor = cipher.encryptor()
    cont = encryptor.update(content) + encryptor.finalize()
    open(file_path, "wb").close()
    f = open(file_path, "wb")
    f.write(cont)
    f.close()


def DES(key, file_path, iv):                        # DES encryption function
    f = open(file_path, "r",encoding='utf-8')
    content = f.read()
    f.close()
    content = content.encode()
    b = len(content)
    if(b % 8 != 0):
        while(b % 8 != 0):
            content += " ".encode()
            b = len(content)
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    cont = encryptor.update(content) + encryptor.finalize()
    open(file_path, "wb").close()
    f = open(file_path, "wb")
    f.write(cont)
    f.close()
