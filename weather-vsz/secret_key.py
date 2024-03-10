import secrets
import string

# Generate a random string of length 32
secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

print(f"SECRET_KEY={secret_key}")