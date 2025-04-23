from cryptography.fernet import Fernet

#To generate a encryption key
key = Fernet.generate_key()
print(key.decode())

