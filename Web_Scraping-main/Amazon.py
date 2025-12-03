from bs4 import BeautifulSoup
import openpyxl

# Read the HTML file
with open('Amazon.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all required divs
divs = soup.find_all('div', class_=['sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16',
                                    'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16',
                                    'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-16-of-20 s-widget sg-col sg-col-12-of-16 s-widget-spacing-large'])

# Open an Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active

# Write headers
sheet.append(['Product_Name', 'Product_Price', 'Product_Reviews','image'])


# Loop through each div
for div in divs:
    # Try to find Product_Name
    product_image_tag = div.find('span', class_="a-section aok-relative s-image-fixed-height")
    if product_image_tag:
        product_image= product_image_tag.img.strip()
    else:
        product_name = ""
        
    product_name_tag = div.find('span', class_='a-size-medium a-color-base a-text-normal')
    if product_name_tag:
        product_name = product_name_tag.text.strip()
    else:
        product_name = ""

    # Try to find Product_Price
    product_price_tag = div.find('span', class_='a-price-whole')
    if product_price_tag:
        product_price = product_price_tag.text.strip()
    else:
        product_price = ""

    # Try to find Product_Reviews
    product_reviews_tag = div.find('span', class_='a-size-base s-underline-text')
    if product_reviews_tag:
        product_reviews = product_reviews_tag.text.strip()
    else:
        product_reviews = ""

    # Write data to Excel
    sheet.append([product_name, product_price, product_reviews])

# Save the workbook
workbook.save('Amazon_Products.xlsx')

