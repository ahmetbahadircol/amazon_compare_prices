from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# Path to your ChromeDriver
chrome_driver_path = "./chromedriver"

options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

# Initialize Selenium WebDriver
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Open Google Lens
    driver.get("https://lens.google.com/")

    clipboard_content = "https://gwbookstore-london.myshopify.com/cdn/shop/files/462573223_9262834060416244_501121334082820458_n_360x.jpg?v=1733260756"

    # Step 2: Click on the "Upload" button (if present)
    input_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/c-wiz/div[2]/div/div[3]/div[2]/c-wiz/div[2]/input",
            )
        )
    )
    input_element.clear()
    input_element.send_keys(clipboard_content)

    search_button = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/c-wiz/div[2]/div/div[3]/div[2]/c-wiz/div[2]/div",
    )
    search_button.click()

    find_source_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[1]/div[2]/span/div[1]/button/span/div",
            )
        )
    )
    find_source_button.click()

    print("!!!!!!")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    lists = soup.find("li", {"class": "anSuc"})
    breakpoint()
    # Step 4: Extract search results
    results = driver.find_elements(
        By.CLASS_NAME, "some-result-class"
    )  # Adjust class name based on the website's HTML
    for result in results:
        print(result.text)  # Print or process the result

finally:
    # Close the browser
    # driver.quit()
    pass
