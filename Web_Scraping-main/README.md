Web Scraping Mini Project

This project contains three small Python programs that demonstrate basic web scraping using Requests, BeautifulSoup, Pandas, and LXML.

1️⃣ Amazon Product Scraper

Reads data from a local HTML file Amazon.html

Extracts:

Product Name

Price

Rating

Saves the output to Amazon_Products.xlsx

2️⃣ Image Scraper

Scrapes images from this website:

https://www.geeksforgeeks.org/binary-search/


Downloads all images found on the page

Saves them inside a folder named Binary Search

3️⃣ Wikipedia Text Extractor

Extracts text from:

https://en.wikipedia.org/wiki/Artificial_intelligence#Intellectual_property


Collects paragraph and list text

Saves the output to wiki.csv

How to Run
1. Install Libraries
pip install requests beautifulsoup4 lxml pandas

2. Run Amazon Scraper
python Amazon.py

3. Run Image Scraper + Wikipedia Extractor
python image_web.py

Output Files

Amazon_Products.xlsx → Product data

Binary Search/ → Downloaded images

wiki.csv → Extracted Wikipedia text

Project Structure
Web_Scraping-main/
│
├── Amazon.html
├── Amazon.py
├── image_web.py
├── Amazon_Products.xlsx
├── wiki.csv
└── README.md
