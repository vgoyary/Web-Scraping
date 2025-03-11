# ScrapeMonster.tech - Big C Web Scraping Assignment

## 1. Approach

This scraper was built to extract product data from Big C Thailand's website. The approach used includes:
- **Fetching Categories**: The script pulls category URLs from Big C’s JSON API.
- **Extracting Product Listings**: Each category JSON response is parsed to get product details.
- **Handling Missing Data**: If the JSON lacks details (e.g., brand, description, weight, delivery methods), Selenium is used to fetch them from the product page.
- **Barcode Extraction**: The barcode is extracted from the image URL.
- **Anti-Scraping Handling**: The script includes request headers to mimic a browser and delays between requests to avoid detection.
- **Data Storage**: The scraped data is stored in a structured JSON file.

## 2. Total Product Count
- Total products listed on the website: 
- Total products successfully scraped: 390

## 3. Duplicate Handling Logic
- The script ensures that previously scraped products are not duplicated by using their **product URL** as a unique identifier.
- If a product exists in the dataset but has updated details (e.g., price changes), the script overwrites the old data.

## 4. Dependencies
Required Libraries: Add them to **requirements.txt**
- `requests`
- `json`
- `selenium`
- `webdriver-manager`
- `beautifulsoup4`
- `pytesseract`
- `Pillow`
- `re`
- `datetime`

## 5. Run Instructions
- Install the required dependencies (see above).
- Ensure you have Google Chrome installed and ChromeDriver is up to date.
- Download and install Tesseract OCR for extracting text from images.
- Download Tesseract
- Update pytesseract.pytesseract.tesseract_cmd in the script to point to your Tesseract installation.
- Run the script:
    ```bash
    pip install -r requirements.txt
    python scraper.py

## 6. Challenges Faced & Solutions

**1. SSL Module Not Found Issue**

- **Problem**: The SSL module was missing in some environments, causing Selenium to fail.
- **Solution**: A workaround was implemented using:
    ```base
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

**2. Missing Data in JSON Response**

- **Problem**: The API response lacked certain details like brand, description, and weight.
- **Solution**: Selenium was used to extract missing details directly from the product page.

**3. Handling Rate Limits**

- **Problem**: Too many rapid requests could lead to temporary IP bans.
- **Solution**: A request delay (`REQUEST_DELAY = 2s`) was added to slow down scraping.

**4. Extracting Promotional Text from Images**

- **Problem**: Some promotional offers (e.g., "Save 17%") were only present in product images.
- **Solution**: OCR (`pytesseract`) was used to scan images and extract promotional text.

## 7. Sample Output

    ```base
    [
        {
            "name": "โครงการหลวง ผักกาดหอมห่อ 300 ก.",
            "price": 35,
            "price_per_unit": "฿35.00\n฿49.00\n/ Packet",
            "weight_info": "N/A",
            "sku": "2000000223032",
            "brand": "ROYAL PROJECT",
            "category": "Royal Project Vegetables",
            "product_url": "https://www.bigc.co.th/en/product/royal-project-lettuce-per-pack",
            "image": "https://st.bigc-cs.com/cdn-cgi/image/format=webp,quality=90/public/media/catalog/product/32/20/2000000223032/thumbnail/2000000223032_1-20250227140017-.jpg",
            "barcode": "2000000223032",
            "description": "ROYAL PROJECT Lettuce...",
            "promotion": [],
            "delivery_methods": ["Express", "NextDay", "Pickup"],
            "date_scraped": "2025-03-11T17:33:47.025838"
        },
        {
            "name": "โครงการหลวง กะหล่ำปลี 400 ก.",
            "price": 39,
            "price_per_unit": "฿39.00/ Packet",
            "weight_info": "N/A",
            "sku": "2000000223056",
            "brand": "ROYAL PROJECT",
            "category": "Royal Project Vegetables",
            "product_url": "https://www.bigc.co.th/en/product/royal-project-cabbage-per-pack",
            "image": "https://st.bigc-cs.com/cdn-cgi/image/format=webp,quality=90/public/media/catalog/product/56/20/2000000223056/thumbnail/2000000223056_1-20250227135941-.jpg",
            "barcode": "2000000223056",
            "description": "ROYAL PROJECT Cabbage...",
            "promotion": [],
            "delivery_methods": ["Express", "NextDay", "Pickup"],
            "date_scraped": "2025-03-11T17:33:49.679520"
        },
        {
            "name": "โครงการหลวง ข้าวโพดหวานสองสี 600 ก.",
            "price": 39,
            "price_per_unit": "฿39.00/ Packet",
            "weight_info": "N/A",
            "sku": "2000002558620",
            "brand": "ROYAL PROJECT",
            "category": "Royal Project Vegetables",
            "product_url": "https://www.bigc.co.th/en/product/royal-project-bi-color-sweet-corn-600-g",
            "image": "https://st.bigc-cs.com/cdn-cgi/image/format=webp,quality=90/public/media/catalog/product/20/20/2000002558620/thumbnail/2000002558620_1-20250227135914-.jpg",
            "barcode": "2000002558620",
            "description": "ROYAL PROJECT Bi-Color Sweet Corn...",
            "promotion": [],
            "delivery_methods": ["Express", "NextDay", "Pickup"],
            "date_scraped": "2025-03-11T17:33:52.420483"
        }
    ]

## Final Notes

- This scraper effectively gathers product data while handling missing fields using Selenium.
- Future improvements could include better CAPTCHA handling and image-based promotional analysis.