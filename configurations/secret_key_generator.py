import os

def generate_secret_key():
    secret_key = os.urandom(32)
    secret_key_hex = secret_key.hex()
    return secret_key_hex

print(generate_secret_key())