from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_html(url):
    """
    Fetch the HTML content of the URL using Selenium with webdriver-manager.
    """
    # Set up Selenium with Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    chrome_options.add_argument('--no-sandbox')

    # Use webdriver-manager to automatically get the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL
        driver.get(url)

        # Optionally wait for the page to load completely
        time.sleep(3)  # Adjust or replace with explicit waits

        # Get the full HTML source of the page
        html_content = driver.page_source
        return html_content

    finally:
        # Close the WebDriver
        driver.quit()
