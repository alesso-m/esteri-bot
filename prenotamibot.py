from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Configuration ===
EMAIL_SENDER = "put your email here"
EMAIL_RECEIVER = "put your email here"
EMAIL_PASSWORD = "get an app password from google account settings"
CHROME_DRIVER_PATH = r"install chromedriver and put the path here"
PRENOTAMI_EMAIL = "your login email here for pretonami"
PRENOTAMI_PASSWORD = "your pretonami password"
LOGIN_URL = "https://prenotami.esteri.it/"
BOOKING_URL = "https://prenotami.esteri.it/Services/Booking/4878"  # Visa booking page

# === Email Notification Function ===
def send_email_notification():
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Prenot@Mi Appointment Available!"
    body = f"An appointment may be available! Check: {BOOKING_URL}"
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()
    print("✅ Notification sent.")

# === Headless Chrome Setup ===
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
# options.add_argument("--headless=new")  # Uncomment when ready to run silently

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

try:
    print("🔐 Logging into Prenot@Mi...")
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='Email']")))

    email_box = driver.find_element(By.CSS_SELECTOR, "input[name='Email']")
    for char in PRENOTAMI_EMAIL:
        email_box.send_keys(char)
        time.sleep(random.uniform(0.05, 0.10))

    time.sleep(random.uniform(0.3, 0.7))

    pw_box = driver.find_element(By.CSS_SELECTOR, "input[name='Password']")
    for char in PRENOTAMI_PASSWORD:
        pw_box.send_keys(char)
        time.sleep(random.uniform(0.05, 0.10))

    submit_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
            "//button[translate(normalize-space(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')='AVANTI' or " +
            "translate(normalize-space(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')='NEXT']"))
    )

    delay = random.uniform(1.0, 2.5)
    print(f"🕒 Waiting {delay:.2f}s before clicking AVANTI...")
    time.sleep(delay)
    ActionChains(driver).move_to_element(submit_btn).pause(0.5).click(submit_btn).perform()

    print("🔍 Waiting for login to complete...")
    WebDriverWait(driver, 15).until(EC.url_contains("/UserArea"))
    print("✅ Logged in.")

    driver.get(BOOKING_URL)
    print("📍 Navigated to booking page. Waiting for response...")

    # Try detecting the popup
    modal_text = ""
    try:
        content_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jconfirm-content"))
        )
        modal_text = content_div.text.lower().strip()
        print("📋 Popup text:", modal_text)
    except TimeoutException:
        print("⚠️ No popup found. Checking for booking page redirect...")

    # Check if modal indicates no appointments
    not_available_phrases = [
        "currently booked", 
        "posti disponibili",
        "sono esauriti",
        "i posti disponibili per il servizio scelto sono esauriti"
    ]

    if any(p in modal_text for p in not_available_phrases):
        print("❌ No appointments currently available.")
    elif modal_text:
        print("🟡 Unrecognized popup — sending notification just in case.")
        send_email_notification()
    else:
        # No popup — check if redirected to booking page
        current_url = driver.current_url
        print(f"🔍 Current URL: {current_url}")
        if "/Services/Booking/4878" in current_url:
            print("🟢 Appointment page loaded! Likely a slot is open.")
            send_email_notification()
        else:
            print("⚠️ No popup and not on expected booking page — unclear state.")

except TimeoutException:
    print("⚠️ Timeout: Something took too long to load.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()
