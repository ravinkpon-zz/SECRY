from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import os


def DAES(key, file_path,iv):             # AES decryption function
    f = open(file_path, "rb")
    content = f.read()
    f.close()
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    content = decryptor.update(content) + decryptor.finalize()
    f = open(file_path, "wb")
    f.write(content)
    f.close()


def DRC4(key, file_path, iv):           # RC4 decryption function
    f = open(file_path, "rb")
    content = f.read()
    f.close()
    backend = default_backend()
    cipher = Cipher(algorithms.ARC4(key), mode=None, backend=backend)
    decryptor = cipher.decryptor()
    content = decryptor.update(content) + decryptor.finalize()
    f = open(file_path, "wb")
    f.write(content)
    f.close()


def DDES(key, file_path, iv):           # DES decryption function
    f = open(file_path, "rb")
    content = f.read()
    f.close()
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    content = decryptor.update(content) + decryptor.finalize()
    f = open(file_path, "wb")
    f.write(content)
    f.close()

