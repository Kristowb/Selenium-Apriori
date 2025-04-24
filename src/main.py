import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
APR_URL = "https://stake.apr.io/"
CHROME_USER_DATA_DIR = r"C:\Users\User\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Default"
STAKE_AMOUNT = "0.0001"

# === Chrome Setup ===
options = Options()
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
options.add_argument(f"--profile-directory={PROFILE_NAME}")
options.add_argument("--disable-blink-features=AutomationControlled")

# Launch Chrome using existing profile
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# === Open Apriori Stake Platform ===
driver.get(APR_URL)
print("Opened Apriori staking page.")
time.sleep(7)  # Let the page load

# === Staking Loop ===
while True:
    try:
        print("Waiting for input field...")
        input_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="number" or @inputmode="decimal"]'))
        )
        input_field.clear()
        input_field.send_keys(STAKE_AMOUNT)

        print("Clicking 'Stake' or 'Swap Stake' button...")
        stake_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//button[contains(text(), "Stake") or contains(text(), "Swap Stake")]'
            ))
        )
        stake_button.click()

        # Switch to Phantom confirmation popup
        print("Waiting for Phantom popup...")
        WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        print("Clicking 'Approve' in Phantom popup...")
        approve_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Approve")]'))
        )
        approve_button.click()

        # Switch back to main page
        driver.switch_to.window(driver.window_handles[0])
        print("Stake confirmed. Waiting before next iteration...")
        time.sleep(10)

    except Exception as e:
        print(f"[!] Error during staking loop: {e}")
        break

input("Press Enter to close browser...")
driver.quit()
