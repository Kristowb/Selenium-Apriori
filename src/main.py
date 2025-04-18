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
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 3)

# === Open Apriori Stake Platform ===
driver.get(APR_URL)
print("Opened Apriori staking page.")
time.sleep(3)

# === Staking Loop ===
while True:
    try:
        # 1. Input stake amount
        print("Filling in stake amount...")
        input_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="number" or @inputmode="decimal"]'))
        )
        input_field.clear()
        input_field.send_keys(STAKE_AMOUNT)

        # 2. Click Stake button (may be "Stake" or "Swap Stake")
        print("Clicking 'Stake' or 'Swap Stake' button...")
        stake_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Stake") or contains(text(), "Swap Stake")]'))
        )
        stake_button.click()

        # 3. Wait for Phantom popup and confirm
        print("Waiting for Phantom confirmation popup...")
        WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        print("Clicking 'Approve' in Phantom popup...")
        approve_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Approve")]'))
        )
        approve_btn.click()

        # Back to staking page
        driver.switch_to.window(driver.window_handles[0])
        print("Stake confirmed. Waiting before next loop...")

        time.sleep(5)  # Wait time before next loop

    except Exception as e:
        print(f"[!] Error during loop: {e}")
        break  # Break the loop if something critical fails

input("Press Enter to close browser...")
driver.quit()
