from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class DynamicHTMLFetcher:
    def __init__(self):
        # Set up Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # Run in headless mode
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        
    def get_dynamic_html(self, url: str, wait_time: int = 5) -> str:
        """
        Fetch HTML content from a dynamic webpage using Selenium.
        
        Args:
            url (str): The URL to fetch
            wait_time (int): Time to wait for the page to load in seconds
            
        Returns:
            str: Complete HTML content after JavaScript execution
        """
        try:
            # Initialize the driver
            driver = webdriver.Chrome(options=self.chrome_options)
            
            # Load the page
            driver.get(url)
            
            # Wait for content to load
            time.sleep(wait_time)
            
            # Get the page source
            html_content = driver.page_source
            
            # Save to file
            with open('webpage.txt', 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            return html_content
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
            
        finally:
            # Always close the driver
            driver.quit()