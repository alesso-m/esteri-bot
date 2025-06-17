This Python script logs into the Italian consulate's Prenotami (Prenot@Mi) booking portal and checks for available national visa appointments (for stays over 90 days). If an appointment is available, it sends an email notification.

**Features:**

Logs into prenotami.esteri.it using your credentials

Navigates to the National Visa appointment booking page

Detects whether appointments are available

Sends an email alert if a slot is detected

Uses basic anti-bot timing



**Setup Instructions**

1. Clone the Repository

git clone https://github.com/yourusername/prenotami-bot.git
cd prenotami-bot

2. Install Dependencies

Requires Python 3.8+

pip install selenium

3. Install ChromeDriver

Download the version of ChromeDriver that matches your installed version of Chrome from:

https://chromedriver.chromium.org/downloads

4. Extract it and update the path in the script:

CHROME_DRIVER_PATH = r"C:\Path\To\chromedriver.exe"

5. Configure the Script

Open the script file and fill in the following configuration variables near the top:

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_RECEIVER = "your_email@gmail.com" # or another email address
EMAIL_PASSWORD = "your_gmail_app_password" # get an app password from google account settings

PRENOTAMI_EMAIL = "your_prenotami_login_email"
PRENOTAMI_PASSWORD = "your_prenotami_password"

6. Run the Bot

python prenotami_final_jconfirm.py

Optional: If you want the browser to stay hidden, uncomment this line in the script:

options.add_argument("--headless=new")

7. Automation (Optional)

You can run this script on a schedule using:

Task Scheduler (Windows)

launchd (macOS)

cron (Linux)

**Notes**

The script is tailored for the San Francisco consulate’s 90+ day visa booking page, but can be adapted for others.

If the site layout changes, the script may break and need to be updated.

This script uses Gmail SMTP to send email alerts. If you use 2FA, generate a Gmail App Password.
