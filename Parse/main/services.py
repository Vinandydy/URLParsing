from http.client import responses
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from django.http import FileResponse
from rest_framework.pagination import PageNumberPagination
import pandas as pd
from io import BytesIO

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

def xlsx_format(queryset):
    df = pd.DataFrame.from_records(queryset.values(), exclude=['time_created', 'time_deleted'])

    export = BytesIO()
    df.to_excel(export, index=False)
    export.seek(0)

    response = FileResponse(
        export,
        as_attachment=True,
        filename='data.xlsx',
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response["Content-Disposition"] = "attachment; filename=data.xlsx"
    return response