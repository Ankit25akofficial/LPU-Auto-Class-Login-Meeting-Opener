import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import threading
import keyring
from datetime import datetime

scheduler_thread = None
is_running = False

def automate_login():
    driver = None
    try:
        username = keyring.get_password("lpu", "username")
        password = keyring.get_password("lpu", "password")
        
        if not username or not password:
            status_label.config(text="❌ No stored credentials found!")
            print("❌ No stored credentials found!")
            return
            
        status_label.config(text="🔄 Opening browser...")
        print(f"🔄 Attempting login at {datetime.now().strftime('%H:%M:%S')}")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
       
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.popups": 2,
            "profile.default_content_settings.popups": 0
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20) 
        status_label.config(text="🔄 Loading LPU portal...")
        driver.get("https://myclass.lpu.in/")
        
        print("Waiting for login form...")
        
        try:
            # Find and fill username (name="i")
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "i")))
            username_field.clear()
            username_field.send_keys(username)
            print(f"Entered username: {username}")
            
            # Find and fill password (name="p")
            password_field = driver.find_element(By.NAME, "p")
            password_field.clear()
            password_field.send_keys(password)
            print("Entered password")
            
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            print("Clicked login button")
        
            time.sleep(3)
            
            try:
                error_invalid = driver.find_element(By.ID, "invalid")
                if "d-none" not in error_invalid.get_attribute("class"):
                    status_label.config(text="❌ Invalid credentials")
                    print("❌ Invalid credentials")
                    return
            except NoSuchElementException:
                pass
                
            try:
                error_blocked = driver.find_element(By.ID, "blocked")
                if "d-none" not in error_blocked.get_attribute("class"):
                    status_label.config(text="❌ Account blocked")
                    print("❌ Account blocked")
                    return
            except NoSuchElementException:
                pass
                
            current_url = driver.current_url.lower()
            if "login" in current_url:
                status_label.config(text="⚠️ Still on login page - check credentials")
                print("⚠️ Login may have failed")
                return
                
            print("✅ Login successful - navigating to class/meeting page")
            status_label.config(text="✅ Logged in - opening class/meeting...")
            
        except TimeoutException:
            status_label.config(text="❌ Timeout: Login form not loaded")
            driver.save_screenshot("login_timeout.png")
            return
        except Exception as e:
            status_label.config(text=f"❌ Login error: {str(e)}")
            print(f"❌ Login error: {str(e)}")
            driver.save_screenshot("login_error.png")
            return
        
        try:
            meeting_url = "https://lovelyprofessionaluniversity.codetantra.com/secure/tla/m.jsp"
            print(f"Navigating to meeting page: {meeting_url}")
            driver.get(meeting_url)
            
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)  #
            
            page_title = driver.title.lower()
            if "tla" in page_title or "meeting" in page_title or "class" in page_title:
                print("✅ Successfully opened class/meeting page")
                status_label.config(text="✅ Class/Meeting page opened!")
            else:
                print("⚠️ Meeting page loaded but title unexpected")
                status_label.config(text="⚠️ Meeting page loaded - check browser")
                
            driver.maximize_window()
            
        except TimeoutException:
            status_label.config(text="❌ Timeout loading meeting page")
            print("❌ Timeout loading meeting page")
            driver.save_screenshot("meeting_timeout.png")
        except Exception as e:
            status_label.config(text=f"❌ Meeting page error: {str(e)}")
            print(f"❌ Meeting page error: {str(e)}")
            driver.save_screenshot("meeting_error.png")
            
        print("Browser remains open with class/meeting page")
        
    except Exception as e:
        error_msg = f"❌ Fatal error: {str(e)}"
        status_label.config(text=error_msg)
        print(error_msg)

def schedule_login():
    global scheduler_thread, is_running
    
    schedule_time = entry_time.get().strip()
    
    try:
        time.strptime(schedule_time, "%H:%M")
    except ValueError:
        status_label.config(text="❌ Invalid time format! Use HH:MM")
        return
    
    if is_running:
        status_label.config(text="⚠️ Scheduler already running!")
        return
        
    is_running = True
    status_label.config(text=f"⏰ Scheduled for {schedule_time}")
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    countdown_label.config(text="")
    
    def wait_and_login():
        global is_running
        while is_running:
            current_time = time.strftime("%H:%M")
            current_seconds = time.strftime("%H:%M:%S")
            root.after(0, lambda: countdown_label.config(text=f"Current time: {current_seconds}"))
            
            if current_time == schedule_time:
                root.after(0, automate_login)
                is_running = False
                root.after(0, lambda: start_button.config(state="normal"))
                root.after(0, lambda: stop_button.config(state="disabled"))
                break
            time.sleep(1)
    
    scheduler_thread = threading.Thread(target=wait_and_login, daemon=True)
    scheduler_thread.start()

def stop_scheduler():
    global is_running
    is_running = False
    status_label.config(text="⏹️ Scheduler stopped")
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    countdown_label.config(text="")

def test_login():
    threading.Thread(target=automate_login, daemon=True).start()

def check_stored_credentials():
    username = keyring.get_password("lpu", "username")
    password = keyring.get_password("lpu", "password")
    if username and password:
        status_label.config(text=f"✅ Credentials found for: {username}")
    else:
        status_label.config(text="❌ No credentials stored")

root = tk.Tk()
root.title("LPU Auto Login + Meeting")
root.geometry("500x420")
root.resizable(False, False)

tk.Label(root, text="LPU Auto Login & Open Meeting", font=("Arial", 16, "bold")).pack(pady=10)

time_frame = tk.Frame(root)
time_frame.pack(pady=10)
tk.Label(time_frame, text="Schedule Time (HH:MM):", font=("Arial", 11)).pack(side="left", padx=5)
entry_time = tk.Entry(time_frame, width=10, font=("Arial", 12))
entry_time.insert(0, time.strftime("%H:%M"))
entry_time.pack(side="left")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
start_button = tk.Button(button_frame, text="▶️ Start Scheduler", command=schedule_login, width=15, bg="#4CAF50", fg="white", font=("Arial", 11))
start_button.pack(side="left", padx=5)
stop_button = tk.Button(button_frame, text="⏹️ Stop", command=stop_scheduler, width=10, bg="#f44336", fg="white", font=("Arial", 11), state="disabled")
stop_button.pack(side="left", padx=5)

status_label = tk.Label(root, text="Ready", font=("Arial", 10), fg="blue")
status_label.pack(pady=5)
countdown_label = tk.Label(root, text="", font=("Arial", 9), fg="gray")
countdown_label.pack()

cred_frame = tk.Frame(root)
cred_frame.pack(pady=20)


# ############################################





def open_credential_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Store Credentials")
    dialog.geometry("350x250")
    dialog.transient(root)
    dialog.grab_set()
    tk.Label(dialog, text="Enter your LPU credentials:", font=("Arial", 11)).pack(pady=10)
    tk.Label(dialog, text="Username (Registration No.):").pack()
    user_entry = tk.Entry(dialog, width=30)
    user_entry.pack(pady=5)
    tk.Label(dialog, text="Password:").pack()
    pass_entry = tk.Entry(dialog, width=30, show="*")
    pass_entry.pack(pady=5)
    def save_credentials():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()
        if username and password:
            keyring.set_password("lpu", "username", username)
            keyring.set_password("lpu", "password", password)
            status_label.config(text="✅ Credentials saved!")
            dialog.destroy()
        else:
            tk.Label(dialog, text="Please fill both fields!", fg="red").pack()
    tk.Button(dialog, text="Save Credentials", command=save_credentials, bg="#2196F3", fg="white").pack(pady=10)

tk.Button(cred_frame, text="🔐 Update Credentials", command=open_credential_dialog, width=18, bg="#2196F3", fg="white").pack(side="left", padx=5)
tk.Button(cred_frame, text="🧪 Test Login + Meeting", command=test_login, width=20, bg="#FF9800", fg="white").pack(side="left", padx=5)
tk.Button(cred_frame, text="🔍 Check Stored", command=check_stored_credentials, width=12, bg="#9C27B0", fg="white").pack(side="left", padx=5)

instructions = tk.Label(
    root, 
    text="1. Update credentials (Registration No. & Password)\n2. Test: Logs in and opens class/meeting page\n3. Schedule auto execution\n\nBrowser stays open after success",
    font=("Arial", 9),
    fg="gray"
)
instructions.pack(pady=10)

root.mainloop()