from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Optional

class HTMLFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_html(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a given URL using urllib.
        
        Args:
            url (str): The URL to fetch HTML from
            
        Returns:
            str: HTML content if successful, None if failed
        """
        try:
            # Create request object with headers
            req = Request(url, headers=self.headers)
            
            # Open URL and read content
            with urlopen(req) as response:
                html_content = response.read().decode('utf-8')
                return html_content
                
        except HTTPError as e:
            print(f"HTTP Error occurred while fetching {url}: {e.code}")
            return None
        except URLError as e:
            print(f"URL Error occurred while fetching {url}: {str(e.reason)}")
            return None
        except Exception as e:
            print(f"Unexpected error occurred while fetching {url}: {str(e)}")
            return None