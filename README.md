# LPU Auto Class Login & Meeting Opener

A simple yet effective Python GUI application built with Selenium and Tkinter to automate the process of logging into the LPU MyClass portal and navigating to the class/meeting page at a user-defined schedule.

 


---

## 🚀 Features

-   **Graphical User Interface (GUI):** Easy-to-use interface built with Tkinter.
-   **Scheduled Execution:** Set a specific time (in HH:MM format) for the script to automatically log in.
-   **Secure Credential Storage:** Uses the `keyring` library to securely store your username and password in your operating system's native credential manager (e.g., Windows Credential Manager, macOS Keychain). Your password is never stored in plain text.
-   **One-Click Testing:** Instantly test the login and meeting-opening process without waiting for the scheduled time.
-   **Status Updates:** The GUI provides real-time feedback on the script's progress, from scheduling to successful login or errors.
-   **Automated Browser Control:** Uses Selenium to handle browser interactions, fill in forms, and click buttons seamlessly.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.x:** [Download Python](https://www.python.org/downloads/)
2.  **Google Chrome:** The script is configured to use the Chrome browser. [Download Chrome](https://www.google.com/chrome/)
3.  **ChromeDriver:** You must have the corresponding ChromeDriver for your version of Google Chrome.
    -   Check your Chrome version by going to `chrome://settings/help`.
    -   Download the matching ChromeDriver from the [Chrome for Testing availability dashboard](https://googlechromelabs.github.io/chrome-for-testing/).

---

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/lpu-auto-class-login.git
    cd lpu-auto-class-login
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install selenium keyring
    ```
    *Note: `tkinter` is usually included with standard Python installations.*

3.  **Set up ChromeDriver:**
    -   **Easy Method:** Download and unzip `chromedriver.exe` and place it in the **same folder** as the Python script.
    -   **Advanced Method:** Place `chromedriver.exe` in a directory and add that directory to your system's `PATH` environment variable.

---

## ▶️ How to Use

1.  **Run the application:**
    ```bash
    python main.py
    ```
    *(Assuming you named your script `main.py`)*

2.  **Store Your Credentials:**
    -   Click the `🔐 Update Credentials` button.
    -   A new window will appear. Enter your LPU Registration Number and Password.
    -   Click `Save Credentials`. This is a one-time setup (unless your password changes).

3.  **Test the Login (Recommended):**
    -   Click the `🧪 Test Login + Meeting` button.
    -   A new Chrome window should open, log you in, and navigate to the meeting page. This confirms your credentials and setup are working.

4.  **Schedule the Login:**
    -   In the "Schedule Time (HH:MM)" box, enter the time you want the script to run (e.g., `08:55` for an 8:55 AM login).
    -   Click the `▶️ Start Scheduler` button.
    -   The application will now monitor the time and execute the login automatically when the scheduled time is reached.
    -   <img width="613" height="564" alt="image" src="https://github.com/user-attachments/assets/bde7def7-a3fb-4656-8f19-101874aab904" />


5.  **Stop the Scheduler:**
    -   To cancel a scheduled task, simply click the `⏹️ Stop` button.

---

## ⚠️ Disclaimer

-   This script is intended for educational and personal convenience purposes only.
-   The user is solely responsible for its usage. The developers are not responsible for any consequences that may arise from using this tool, such as missing a class due to a script failure.
-   Websites can change their structure at any time, which may break this script. It may require updates to continue functioning.
-   This project is not affiliated with, endorsed by, or sponsored by Lovely Professional University.
