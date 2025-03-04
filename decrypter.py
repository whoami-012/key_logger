from cryptography.fernet import Fernet
import json

logs_file = "logs.enc"
key_file = "secret.key"

# Load encryption key
with open(key_file, "rb") as file:
    key = file.read()

cipher = Fernet(key)

# Read & decrypt logs
with open(logs_file, "rb") as file:
    encrypted_data = file.read()
    decrypted_logs = json.loads(cipher.decrypt(encrypted_data).decode())

# Print logs
for entry in decrypted_logs:
    print(entry)
