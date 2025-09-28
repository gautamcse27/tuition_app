from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Print the generated key string for copy-pasting
