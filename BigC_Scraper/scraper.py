import requests
import json
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Base URL for category JSON data
BASE_URL = "https://www.bigc.co.th/_next/data/ygIhKgGTvvJ-jNQIx3BY5/en/category/"
OUTPUT_FILE = "products.json"
REQUEST_DELAY = 2  # Time delay to avoid detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# Category slugs for constructing JSON request URLs
CATEGORIES = {
    "Grocery & Bakery": "grocery-bakery",
    "Beverages": "beverages",
    "Pantry & Ingredients": "pantry-and-ingredients",
    "Snacks & Desserts": "snacks-and-desserts"
}

def extract_barcode(thumbnail_url):
    #Extracts the barcode number from the thumbnail URL.
    match = re.search(r'/(\d{12,13})/', thumbnail_url)
    return match.group(1) if match else "N/A"

def setup_driver():
    #Initialize the Selenium WebDriver.
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_missing_details(product_url, driver, max_retries=2):
    #Scrape missing details from the product page using Selenium, with detailed logging.
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            print(f"[{datetime.now()}] Fetching product details: {product_url} (Attempt {attempt+1}/{max_retries})")

            driver.set_page_load_timeout(30)  # Reduce timeout from 120s to 30s
            driver.get(product_url)
            time.sleep(2)  # Allow time for the page to load

            try:
                name = driver.find_element(By.CSS_SELECTOR, "h1#pdp_product-title").text.strip()
            except:
                name = "N/A"

            try:
                description = driver.find_element(By.CSS_SELECTOR, "#pdp_desktop-desc .description_desc__7MwoO").text.strip()
            except:
                description = "N/A"

            try:
                brand = driver.find_element(By.CSS_SELECTOR, "#pdp_brand-title").text.strip()
            except:
                brand = "N/A"

            try:
                category = driver.find_element(By.CSS_SELECTOR, "#pdp_category-title a").text.strip()
            except:
                category = "N/A"

            try:
                price_per_unit = driver.find_element(By.CSS_SELECTOR, "#pdp_product-price-new .productDetail_product_price_new__TKGLM").text.strip()
            except:
                price_per_unit = "N/A"

            try:
                weight_info = driver.find_element(By.CSS_SELECTOR, "#pdp_product-sellInKg .productDetail_weight-description__zPT27").text.strip()
            except:
                weight_info = "N/A"

            # Extract delivery methods
            delivery_methods = []
            try:
                delivery_sections = driver.find_elements(By.CSS_SELECTOR, ".shipping_section_shipping__bOz4_ .shipping_shipping_item__bzHrT")
                for method in delivery_sections:
                    delivery_methods.append(method.text.strip())
            except:
                delivery_methods = []

            end_time = time.time()
            print(f"[{datetime.now()}] Successfully scraped {name} (Time taken: {round(end_time - start_time, 2)}s)")

            return name, description, brand, category, price_per_unit, weight_info, delivery_methods

        except Exception as e:
            print(f"[{datetime.now()}] Error scraping {product_url}: {str(e)}")
            if attempt + 1 < max_retries:
                print(f"[{datetime.now()}] Retrying in 5 seconds...")
                time.sleep(5)

    print(f"[{datetime.now()}] Skipping {product_url} after {max_retries} failed attempts")
    return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", []

def fetch_products(category_name, category_slug, driver):
    #Fetch all products from the category, handling pagination with detailed logs.
    page = 1
    all_products = []

    while True:
        url = f"{BASE_URL}{category_slug}.json?page={page}"
        print(f"[{datetime.now()}] Fetching {category_name} - Page {page}...")

        try:
            start_time = time.time()
            response = requests.get(url, headers=HEADERS, timeout=10)
            response_time = round(time.time() - start_time, 2)

            if response.status_code != 200:
                print(f"[{datetime.now()}] Failed to fetch {url} (Status: {response.status_code})")
                break

            data = response.json()
            products_data = data.get("pageProps", {}).get("productCategory", {}).get("products_summary", {}).get("products", [])

            if not products_data:
                print(f"[{datetime.now()}] No more products found for {category_name} on page {page}.")
                break

            print(f"[{datetime.now()}]  Fetched {len(products_data)} products (Response time: {response_time}s)")

            for product in products_data:
                thumbnail_url = product.get("thumbnail_image", "N/A")
                barcode = extract_barcode(thumbnail_url)
                product_url = f'https://www.bigc.co.th/en/product/{product.get("slug", "")}'

                print(f"[{datetime.now()}]  Scraping: {product_url}")
                name, description, brand, category, price_per_unit, weight_info, delivery_methods = scrape_missing_details(product_url, driver)

                all_products.append({
                    "name": name,
                    "price": product.get("final_price_incl_tax", "N/A"),
                    "price_per_unit": price_per_unit,
                    "weight_info": weight_info,
                    "sku": barcode,
                    "brand": brand,
                    "category": category,
                    "product_url": product_url,
                    "image": thumbnail_url,
                    "barcode": barcode,
                    "description": description,
                    "promotion": product.get("price", {}).get("promotions", []),
                    "delivery_methods": delivery_methods,
                    "date_scraped": datetime.now().isoformat()
                })

            page += 1
            time.sleep(REQUEST_DELAY)

        except requests.exceptions.Timeout:
            print(f"[{datetime.now()}] Timeout occurred while fetching {url}, retrying...")
            time.sleep(5)
            continue

        except Exception as e:
            print(f"[{datetime.now()}] Error fetching data for {category_name}: {str(e)}")
            break

    return all_products

def main():
    all_data = []
    driver = setup_driver()

    for category_name, category_slug in CATEGORIES.items():
        print(f"\n[{datetime.now()}]  Starting Scraper for {category_name}")
        category_products = fetch_products(category_name, category_slug, driver)
        all_data.extend(category_products)

    driver.quit()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"\n[{datetime.now()}] Scraped {len(all_data)} total products!")

if __name__ == "__main__":
    main()
