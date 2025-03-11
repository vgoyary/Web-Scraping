# ScrapeMonster.tech - Big C Web Scraping Assignment  

## 1️. Approach Used  
### Step-by-Step Process:  
 **Fetching Categories & Subcategories:**  
- Extracted product categories from Big C’s structured JSON API.  
- Identified subcategories and recursively scraped them.  

 **Handling Pagination:**  
- Implemented pagination to iterate through all pages of each category.  
- Stopped pagination automatically when no more products were found.  

 **Fetching Product Data:**  
- Extracted **product name, price, barcode, brand, category, description, delivery methods, and promotions** using a combination of API and Selenium.  
- Used **Selenium** to scrape missing details from the product page.  

 **Handling Anti-Scraping Protections:**  
- **Added random delays** between requests to prevent detection.  
- **Implemented retry logic** for failed page loads.  
- **Used a realistic User-Agent header** to mimic human browsing.  
---
## 2. Total Product Count
- Total products listed on the website: 
- Total products successfully scraped: 390
---
## 3️. Duplicate Handling Logic  
 **Prevents scraping the same product twice:**  
- Uses **product URLs and SKUs** to check for duplicates.  
- Ensures only new products are scraped on each run.  

 **Handling Updates to Existing Products:**  
- If a product is already scraped, it updates **price, promotions, and availability** in the output JSON file.  

---
## 4. Dependencies
- Required Libraries: Add them to **requirements.txt**
  - `requests`
  - `json`
  - `selenium`
  - `webdriver-manager`
  - `beautifulsoup4`
  - `pytesseract`
  - `Pillow`
  - `re`
  - `datetime`
---
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

**1. Missing Data in JSON Response**

- **Problem**: The API response lacked certain details like brand, description, and weight.
- **Solution**: Selenium was used to extract missing details directly from the product page.

**2. Handling Rate Limits**

- **Problem**: Too many rapid requests could lead to temporary IP bans.
- **Solution**: A request delay (`REQUEST_DELAY = 2s`) was added to slow down scraping.

**3. Extracting Promotional Text from Images**

- **Problem**: Some promotional offers (e.g., "Save 17%") were only present in product images.
- **Solution**: OCR (`pytesseract`) was used to scan images and extract promotional text.

**4.Slow Page Loading & Timeouts**

- **Problem**: Some product pages took too long to load, causing Selenium timeouts.
- **Solution**: Set `driver.set_page_load_timeout(30)` to avoid excessive wait times. Implemented **automatic retries (up to 2 times)** for failed pages.

**5. Captchas / Blocking Issues**

- **Problem**: Too many requests triggered anti-bot measures.
- **Solution**: Slowed down requests using `time.sleep(5)`. Used realistic **User-Agent headers** to mimic human behavior.

**6. Handling Promotions & Delivery Methods**

- **Problem**: Some products had missing promotions or delivery details.
- **Solution**: **Extracted details from the product page** using Selenium. **Ensured empty fields default** to `"N/A"` instead of breaking the script.
---
## 7. Sample Output
  
- First three outputs
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
---
## Final Notes

- This scraper effectively gathers product data while handling missing fields using Selenium.
- Future improvements could include better CAPTCHA handling and image-based promotional analysis.

## Contributing
If you want to contribute to this project, please feel free to fork the repository and create a pull request with your changes.

## Contact
If you have any questions or queries please contact me at **<a href="vileenagoyary02@gmail.com" style="color: blue;">vileenagoyary02@gmail.com</a>**.