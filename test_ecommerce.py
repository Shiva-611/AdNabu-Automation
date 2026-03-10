from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

# Create reports folder if not exists
if not os.path.exists("reports"):
    os.makedirs("reports")

# HTML report file
report_file = f"reports/report.html"

driver = webdriver.Chrome()

def write_report(message):
    with open(report_file, "a") as f:
        f.write(f"<p>{datetime.now().strftime('%H:%M:%S')} - {message}</p>\n")

def wait_for_page_load():
    try:
        driver.set_page_load_timeout(20)
        write_report("Page loaded successfully")
    except Exception as e:
        write_report(f"Page did not load: {e}")

def ecommerce_code():
    try:
        driver.get("https://adnabu-store-assignment1.myshopify.com/password")
        wait_for_page_load()
        driver.maximize_window()

        # Enter password
        password = driver.find_element(By.XPATH, "//input[@type='password']")
        password.send_keys("AdNabuQA")
        enterBtn = driver.find_element(By.XPATH, "//button[@type='submit']")
        enterBtn.click()
        write_report("Password entered and submitted")

        # Search product
        searchBtn = driver.find_element(By.XPATH,"//summary[@aria-label='Search']")
        searchBtn.click()
        search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        search_input.send_keys("The Complete Snowboard")
        search_submit = driver.find_element(By.XPATH,"//button[@class='search__button field__button' and not(@type='submit')]")
        search_submit.click()
        write_report("Searched for 'The Complete Snowboard'")

        # Click product
        item = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH,"//div[contains(@class, 'card-wrapper') and .//a[contains(text(), 'The Complete Snowboard')]]"))
        )
        item.click()
        write_report("Product clicked")

        # Add to cart
        addToCart = driver.find_element(By.XPATH,"//button[@name='add']")
        addToCart.click()
        write_report("Clicked 'Add to Cart'")

        # Verify checkout
        checkout = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@name='checkout']"))
        )
        if checkout.is_displayed():
            write_report("The product is Added to the Cart Successfully!")
        else:
            write_report("The product is NOT added to the cart")

    except Exception as e:
        write_report(f"Test failed: {e}")
    finally:
        driver.quit()
        write_report("Browser closed")

# Run the test
ecommerce_code()
print(f"Report generated: {report_file}")