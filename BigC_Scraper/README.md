# Big C Scraper - ScrapeMonster.tech

## 1. Approach
This scraper extracts product data from BigC Thailand's website using their Next.js JSON API (`_next/data/...`). Instead of scraping HTML, it directly fetches structured JSON data, making the process faster and more reliable.

#### Steps Followed:
- Constructed API request URLs for each category.
- Sent requests to fetch category JSON data.
- Extracted relevant product details from pageProps.
- Processed product name, price, SKU, category, product URL, and image.
- Introduced a delay between requests to avoid detection.
- Saved results in products.json

## 2. Total Product Count
- Total products listed on the website: (To be filled after full scrape)
- Total products successfully scraped: (To be filled after execution)

## 3. Duplicate Handling Logic
- CThe script ensures that each product is uniquely identified by its product URL.
- Skipped already scraped unless data changed.

## Dependencies
- Python 3.9+
- Requests, BeautifulSoup4, Selenium, WebDriver-Manager

## Run Instructions
```bash
pip install -r requirements.txt
python scraper.py
