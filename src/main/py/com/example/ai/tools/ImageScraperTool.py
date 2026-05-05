from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup

class ImageScraperTool(BaseTool):
    name: str = "Image Scraper Tool"
    description: str = "Extracts image URLs from a given website"

    def _run(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        
        # Extract src attribute from each img tag
        image_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
        return ", ".join(image_urls)