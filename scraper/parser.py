import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

# Automatically download and manage ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def parse_home(html_content):
    """
    Parse the HTML content using BeautifulSoup and extract data.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    data = []

    # Extract titles and links
    for item in soup.select("a.gui-button-container"):  # Adjust selectors as needed
        title = item.text.strip()  # Extract the visible text
        link = item["href"]       # Extract the href attribute
        data.append(link)

    return data

def scrape_page_with_selenium(url, selectors):
    """
    Fetch and scrape a single page using Selenium to handle dynamic content.

    :param url: The URL of the page to scrape.
    :param selectors: A dictionary of CSS selectors to extract data.
    :return: A dictionary containing the extracted data.
    """
    try:
        driver.get(url)

        # Wait for the first element to be located to ensure the page is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, next(iter(selectors.values()))))
        )

        data = {}
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        # Get the value of 'idAnnuncio'
        id_annuncio = query_params.get("idAnnuncio", [None])[0]
        data["Id"] = id_annuncio
        data["URL"] = url

        # Iterate over selectors
        for key, selector in selectors.items():
            try:
                if key == "Tribunale":
                    # Locate all parent containers
                    containers = driver.find_elements(By.CSS_SELECTOR, selector)
                    found_value = False
                    for container in containers:
                        try:
                            # Check if the title matches "Tribunale"
                            title_element = container.find_element(By.CSS_SELECTOR, "div.gui-text-tile-title")
                            if "Tribunale" in title_element.text.strip():
                                # Extract the corresponding bold text
                                value_element = container.find_element(By.CSS_SELECTOR,
                                                                       "div.gui-text-tile-text.text-bold")
                                data[key] = value_element.text.strip()
                                found_value = True
                                break
                        except Exception as e:
                            print(f"Error while processing '{key}' in a container: {e}")

                    if not found_value:
                        data[key] = None

                elif key == "Data Vendita":
                    # Similar logic for "Data Vendita"
                    containers = driver.find_elements(By.CSS_SELECTOR, selector)
                    found_value = False
                    for container in containers:
                        try:
                            title_element = container.find_element(By.CSS_SELECTOR, "div.gui-text-tile-title")
                            if "Data di vendita" in title_element.text.strip():
                                value_element = container.find_element(By.CSS_SELECTOR,
                                                                       "div.gui-text-tile-text.text-bold")
                                data[key] = value_element.text.strip()
                                found_value = True
                                break
                        except Exception as e:
                            print(f"Error while processing '{key}' in a container: {e}")

                    if not found_value:
                        data[key] = None

                elif key == "N° Procedura":
                    # Locate containers matching the main selector
                    containers = driver.find_elements(By.CSS_SELECTOR, selector)
                    found_value = False
                    for container in containers:
                        try:
                            # Find the label element
                            label_element = container.find_element(By.CSS_SELECTOR, "div.gui-text-tile-title")
                            if "N° Procedura" in label_element.text.strip():
                                # Find the sibling value element
                                value_element = container.find_element(By.CSS_SELECTOR,
                                                                       "div.gui-text-tile-text.text-bold")
                                data[key] = value_element.text.strip()
                                found_value = True
                                break
                        except Exception as e:
                            print(f"Error while processing '{key}' in a container: {e}")

                    if not found_value:
                        data[key] = None

                elif key == "Anno Procedura":
                    # Locate containers matching the main selector
                    containers = driver.find_elements(By.CSS_SELECTOR, selector)
                    found_value = False
                    for container in containers:
                        try:
                            # Find the label element
                            label_element = container.find_element(By.CSS_SELECTOR, "div.gui-text-tile-title")
                            if "Anno Procedura" in label_element.text.strip():
                                # Find the sibling value element
                                value_element = container.find_element(By.CSS_SELECTOR,"div.gui-text-tile-text.text-bold")
                                data[key] = value_element.text.strip()
                                found_value = True
                                break
                        except Exception as e:
                            print(f"Error while processing '{key}' in a container: {e}")

                    if not found_value:
                        data[key] = None

                elif key == "N° Procedura":
                    # Use a valid selector for the container
                    containers = driver.find_elements(By.CSS_SELECTOR, "gui-text-tile")
                    found_value = False
                    for container in containers:
                        try:
                            # Check for label matching 'N° Procedura'
                            label_element = container.find_element(By.CSS_SELECTOR, "div.gui-text-tile-title")
                            if "N° Procedura" in label_element.text.strip():
                                # Extract value from sibling element
                                value_element = container.find_element(By.CSS_SELECTOR,
                                                                       "div.gui-text-tile-text.text-bold")
                                data[key] = value_element.text.strip()
                                found_value = True
                                break
                        except Exception as e:
                            print(f"Error while processing '{key}' in a container: {e}")

                    if not found_value:
                        data[key] = None

                elif key == "Tipologia":
                    # Similar logic for "Data Vendita"
                    containers = driver.find_elements(By.CSS_SELECTOR, selector)
                    found_value = False
                    for container in containers:
                        try:
                            label_element = container.find_element(By.CSS_SELECTOR, "div.col-4.text-semibold.corpus-s")
                            if "Tipologia" in label_element.text.strip():
                                # Find the sibling value element
                                value_element = container.find_element(By.CSS_SELECTOR, "div.col-8.corpus-s")
                                data[key] = value_element.text.strip()
                                found_value = True
                                break
                        except Exception as e:
                            print(f"Error while processing '{key}' in a container: {e}")

                    if not found_value:
                        data[key] = None

                else:
                    # General case for other keys
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        data[key] = elements[0].text.strip()
                    else:
                        data[key] = None

                print(f"Extracted text for '{key}': {data.get(key)}")

            except Exception as e:
                data[key] = None
                print(f"Could not find element for selector '{selector}' or error occurred: {e}")

        return data

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_multiple_pages(href_list, selectors):
    """
    Navigate to each URL in the href_list and scrape data using selectors.

    :param href_list: List of URLs to scrape.
    :param selectors: A dictionary of CSS selectors to extract data.
    :return: A list of dictionaries containing the scraped data from each page.
    """
    scraped_data = []
    for url in href_list:
        page_data = scrape_page_with_selenium(url, selectors)
        print(f"Scraping: {page_data}")
        if page_data:
            scraped_data.append(page_data)

    return scraped_data

# Example usage
if __name__ == "__main__":
    try:
        # Example list of href links
        href_list = [
            "https://example.com/page1",
            "https://example.com/page2",
        ]

        # Example selectors
        selectors = {
            "title": "h1.page-title",
            "description": "div.page-description",
            "price": "span.price"
        }

        # Scrape data from all pages
        results = scrape_multiple_pages(href_list, selectors)

        # Print the scraped data
        for result in results:
            print(result)

    finally:
        # Ensure the driver is properly closed after scraping all pages
        driver.quit()
