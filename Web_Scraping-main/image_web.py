import requests
from bs4 import BeautifulSoup
import os
import csv
from urllib.parse import urljoin, urlparse

# ------------------------------------------------------------
# IMAGE SCRAPING FUNCTION (IMPROVED)
# ------------------------------------------------------------
def scrape_images(url, save_folder):
    # Create a directory to save images if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # Fetch the HTML content of the webpage
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch webpage: {url} (status code: {response.status_code})")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img tags
    img_tags = soup.find_all('img')

    downloaded = set()
    count = 0

    for i, img_tag in enumerate(img_tags, start=1):
        # Try different common attributes
        img_url = (
            img_tag.get('src')
            or img_tag.get('data-src')
            or img_tag.get('data-lazy-src')
            or img_tag.get('data-original')
        )

        # Handle srcset (pick the first URL)
        if not img_url and img_tag.get('srcset'):
            srcset = img_tag.get('srcset').split(',')
            if srcset:
                img_url = srcset[0].split()[0].strip()

        if not img_url:
            continue  # nothing usable here

        # Build absolute URL
        img_url = urljoin(url, img_url)

        # Avoid downloading the same image multiple times
        if img_url in downloaded:
            continue
        downloaded.add(img_url)

        try:
            img_response = requests.get(img_url, headers=headers, stream=True, timeout=10)
            if img_response.status_code == 200:
                # Decide filename
                parsed = urlparse(img_url)
                filename = os.path.basename(parsed.path)
                if not filename:  # if URL ends with / or empty
                    filename = f"image_{i}.jpg"

                img_path = os.path.join(save_folder, filename)

                with open(img_path, 'wb') as img_file:
                    for chunk in img_response.iter_content(1024):
                        img_file.write(chunk)

                count += 1
                print(f"Downloaded: {img_path}")
            else:
                print(f"Failed to download (status {img_response.status_code}): {img_url}")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")

    print(f"\nTotal images downloaded: {count}")


# Example usage
url = 'https://www.geeksforgeeks.org/binary-search/'
save_folder = 'Binary Search'
scrape_images(url, save_folder)



# ------------------------------------------------------------
# TEXT EXTRACTOR FOR WIKIPEDIA (SAME AS BEFORE)
# ------------------------------------------------------------
def Extract(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch webpage: {url} (status code: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, 'lxml')

        # Main content on Wikipedia is inside this div
        content_div = soup.find('div', id='mw-content-text')
        if content_div is None:
            print("Content not found on the page.")
            return

        lines = []

        # Extract paragraph text and list items
        for tag in content_div.find_all(['p', 'li']):
            text = tag.get_text(strip=True)
            if text:
                lines.append(text)

        # Save to wiki.csv
        with open("wiki.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Text"])  # header row
            for line in lines:
                writer.writerow([line])

        print("wiki.csv created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


# Run Extract function
Extract('https://en.wikipedia.org/wiki/Artificial_intelligence#Intellectual_property')
