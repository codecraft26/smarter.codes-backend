import requests
from bs4 import BeautifulSoup

def fetch_and_clean_html(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary elements
    for script in soup(["script", "style", "noscript"]):
        script.decompose()

    text = soup.get_text(separator=' ')
    return ' '.join(text.split())
