from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os 
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def scrapping_the_website(website):
    print("Launching the chrome automated browser")
    # Use local driver setup if proxy is not required
    options = Options()
    options.headless = False  # Set to True if you want to run the browser in headless mode
    service = Service(os.environ.get('CHROMEDRIVER_PATH'))

    with webdriver.Chrome(service=service, options=options) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Waiting for captcha...')
        # Add code for CAPTCHA solving if needed
        print('Captcha solved!')
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html  # Return the HTML content

def remove_dom_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body  # Grab the body content
    if body_content:
        return str(body_content)  # Convert body content to string NOTE: DO NOT PUT body_content.text in str as it will remove the new line
    return ""

def unwanted_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for tags in soup(['script', 'style']):  # Remove <script> and <style> elements
        tags.extract()
    
    # Get all text in one line, separated by newlines
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    # Split the content into batches of max_length characters
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]
