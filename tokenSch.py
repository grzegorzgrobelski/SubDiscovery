from playwright.sync_api import sync_playwright
import json
import urllib.parse
from datetime import datetime, timedelta
import time
import os


email = "email"
password = "haslo"


def get_expiry_datetime(expires_str):
    ts = int(expires_str)
    return datetime.fromtimestamp(ts)

def get_refresh_delay_seconds(expires_str):
    expiry_dt = get_expiry_datetime(expires_str)
    refresh_dt = expiry_dt - timedelta(minutes=10)

    now = datetime.now()

    delay = (refresh_dt - now).total_seconds()

    if delay < 0:
        return 0

    return delay


def load_session_data(filename="session_data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return None



def save_session_data(session_data, filename="session_data.json", retries=5, delay=10):
    """
    Zapis pliku z retry jeśli plik jest używany
    """
    for attempt in range(retries):
        try:
            tmp_file = filename + ".tmp"

            with open(tmp_file, "w") as f:
                json.dump(session_data, f, indent=4)

            # atomic replace (bezpieczne)
            os.replace(tmp_file, filename)

            print(f"✅ Zapisano {filename}")
            return True

        except PermissionError:
            print(f"⚠️ Plik zajęty... próba {attempt+1}/{retries}")

            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("❌ Nie udało się zapisać pliku")
                return False



def login_and_save():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.fitatu.com/app/login", timeout=60000)

        # cookies
        page.evaluate("""
            document.querySelector(".cookies-consent-button--primary")?.click();
        """)

        # login
        page.fill("input[type=email]", email)
        page.fill("input[type=password]", password)

        page.evaluate("""
            document.querySelector("button.page-login__submit-button")?.click();
        """)

        page.wait_for_timeout(5000)

        cookies = context.cookies()
        user_cookie = next((c for c in cookies if c["name"] == "user"), None)

        session_data = None

        if user_cookie:
            decoded = urllib.parse.unquote(user_cookie["value"])
            user = json.loads(decoded)

            session_data = {
                "bearer_token": user.get("token"),
                "refresh_token": user.get("refresh_token"),
                "fitatu_user_id": str(user.get("id")),
                "expires": str(user.get("expiredTimestamp"))
            }

        if session_data:
            save_session_data(session_data)

        browser.close()

    return session_data

def run_scheduler():
    while True:
        try:
            data = load_session_data()

            if not data:
                print("⚠️ No session, logging in...")
                login_and_save()
                time.sleep(2)
                continue

            expires = data.get("expires")

            if not expires:
                print("⚠️ No expires → login")
                login_and_save()
                time.sleep(2)
                continue

            delay = get_refresh_delay_seconds(expires)
            expiry_dt = get_expiry_datetime(expires)

            print(f"✅ Token valid until: {expiry_dt}")
            print(f"🕒 Refresh in {delay/60:.2f} min")

            if delay <= 0:
                print("🔄 Refresh now")
                login_and_save()
                time.sleep(2)
                continue

            time.sleep(delay)

        except Exception as e:
            print("❌ Error:", e)
            print("Retry in 60s...")
            time.sleep(60)


if __name__ == "__main__":
    run_scheduler()





