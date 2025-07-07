from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from rest_framework.pagination import PageNumberPagination


def partial(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.title.string if soup.title else "No title"

        favicon = None
        icon_link = soup.find("link", rel=lambda x: x and x.lower() in ["icon", "shortcut icon"])
        if icon_link:
            favicon = urljoin(url, icon_link['href'])

        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")

        return {
            "url": url,
            "name": name,
            "favicon": favicon,
            "description": description,
        }
    except Exception as e:
        return {
            "error": str(e),
            "url": url
        }


class CustomPagination(PageNumberPagination):
    page_size = 10