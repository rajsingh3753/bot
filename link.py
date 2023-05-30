from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc

import json



## Set Chrome Options
options = uc.ChromeOptions()

mobile_emulation = { "deviceName": "iPhone X" }


options.add_argument('--blink-settings=imagesEnabled=false')
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option('prefs', {
    'profile.managed_default_content_settings': {
        'geolocation': 1
    }
})
## Create Undetected Chromedriver with Options
driver = uc.Chrome(options=options)



# Set the path to the cookies.txt file
cookies_file_path = "cookies.json"



# Open the Paytm payment link creation page
driver.get("https://dashboard.paytm.com/next/payment-link/create/quick")
driver.delete_all_cookies()


# Read the cookies from the JSON file
with open(cookies_file_path, 'r') as file:
    cookies = json.load(file)

# Load the cookies into the browser session
for cookie in cookies:
    if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
        cookie["sameSite"] = "None"
    driver.add_cookie(cookie)

# Refresh the page to apply the cookies
driver.refresh()
wait = WebDriverWait(driver, 100)

driver.find_element(By.XPATH, "//button[contains(text(), 'Create Payment link')]").click()


# Wait for the page to load and the required elements to be present

wait.until(EC.presence_of_element_located((By.ID, "linkDescription")))
wait.until(EC.presence_of_element_located((By.ID, "amount")))

# Enter the required information to generate the payment link
amount = "100"
purpose = "Test Payment"

# Fill in the form fields
driver.find_element(By.ID, "amount").send_keys(amount)
driver.find_element(By.ID, "linkDescription").send_keys(purpose)

# Click on the "Create Payment Link" button
driver.find_element(By.XPATH, "//button[contains(text(), 'Create Payment Link')]").click()


# Wait for the payment link to be generated
wait.until(EC.presence_of_element_located((By.ID, "linkDetail")))

# Get the generated payment link
payment_link = driver.find_element(By.ID, "linkDetail").text
print(payment_link)

# Close the browser
driver.quit()
