import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def download_images(topic, num):
    search_query = topic
    num_images = num  # Number of images to download

    # Create directory for images
    os.makedirs(search_query, exist_ok=True)

    # Fetch and download images
    query = search_query
    url = f"https://unsplash.com/s/photos/{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    img_tags = soup.find_all("img")
    count = 0
    for i, img in enumerate(img_tags[:num_images]):
        img_url = img.get("data-src") or img.get("src")  # Use data-src if available, else use src
        if img_url and img_url.startswith("http"):
            img_response = requests.get(img_url)
            with open(os.path.join(search_query, f"image_{i + 1}.jpg"), "wb") as f:
                f.write(img_response.content)
                count += 1
                print(f"Image {count} downloaded")