# lpu_auto_join_pro.py
import os
import sys
import time
import threading
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import win32api
import win32con
import win32gui
import keyring  # Secure password storage

# Configuration
LPU_URL = "https://myclass.lpu.in/"
SCHEDULE_TIME = "02:27"
LOG_FILE = "log.txt"

# Function to log messages
def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# Function to get stored password securely
def get_password():
    try:
        return keyring.get_password("LPU_Auto_Join", "user")
    except Exception as e:
        log(f"🔐 Error retrieving password: {e}")
        return None

# Function to save password securely
def save_password(username, password):
    try:
        keyring.set_password("LPU_Auto_Join", "user", password)
        log("🔐 Password saved securely using Windows Credential Manager.")
    except Exception as e:
        log(f"❌ Failed to save password: {e}")

# Function to automate login
def automate_login():
    username = input("Enter LPU ID: ").strip()
    password = input("Enter LPU Password: ").strip()

    # Save password securely
    save_password(username, password)

    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")

        # Initialize driver
        service = Service(executable_path='chromedriver.exe')
        driver = webdriver.Chrome(executable_path="build/chrome-win64/chromedriver.exe")

        # Open portal
        driver.get(LPU_URL)
        log("🔗 Opening LPU portal...")

        # Wait and fill credentials
        time.sleep(3)
        driver.find_element(By.ID, "txtUser").send_keys(username)
        driver.find_element(By.ID, "txtPass").send_keys(password)
        driver.find_element(By.ID, "btnLogin").click()
        log("✅ Login successful!")

        # Keep browser open for 10 seconds
        time.sleep(10)
        driver.quit()

    except Exception as e:
        log(f"❌ Login failed: {str(e)}")
        if "404" in str(e):
            log("⚠️ Check if URL is correct or ChromeDriver is up to date.")
        elif "timeout" in str(e):
            log("⚠️ Page took too long to load. Check internet connection.")

# Function to check time and trigger login
def schedule_task():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == SCHEDULE_TIME:
            log("⏰ It's 9:00 AM! Starting login...")
            automate_login()
            break
        time.sleep(30)  # Check every 30 seconds

# Function to run in background (no GUI)
def run_background():
    log("🚀 LPU Auto-Join Tool Started - Silent Mode")
    
    # If no password is stored, prompt user once
    stored_pw = get_password()
    if not stored_pw:
        log("🔐 No stored password found. Please enter credentials.")
        automate_login()
    else:
        log("🔐 Using stored password from Windows Credential Manager.")

    # Start scheduling loop
    schedule_task()

# Main entry point
if __name__ == "__main__":
    # Hide console window (for .exe)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        win32gui.SetForegroundWindow(hwnd)

    # Run the task
    run_background()

# PyInstaller command used for packaging:
# pyinstaller --onefile --windowed --name "LPU Auto-Join" --add-data "build/chrome-win64/chromedriver.exe;." lpu_auto_join_pro.py