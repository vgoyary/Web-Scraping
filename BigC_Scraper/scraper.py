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
    "Snacks & Desserts": "snacks-and-desserts",
    "Beauty & Personal Care": "beauty-personal-care",
    "Mom & Baby": "mom-baby",
    "Household Essentials": "household-essentials",
    "Home & Lifestyle": "home-lifestyle",
    "Stationery & Office Supplies": "stationery-and-office-supplies",
    "Pet Food & Supplies": "pet-food-and-pet-supplies",
    "Home Appliances & Electronics": "home-appliances-electronic-products",
    "Fashion & Accessories": "fashion-and-accessories",
    "Pure Pharmacy": "pure-pharmacy"
}


def get_total_products(category_slug):
    #Fetch total product count for a given category.
    url = f"https://www.bigc.co.th/_next/data/ygIhKgGTvvJ-jNQIx3BY5/en/category/{category_slug}.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        total_products = data.get("pageProps", {}).get("productCategory", {}).get("products_summary", {}).get("total",
                                                                                                              0)
        return total_products
    return 0

def extract_barcode(thumbnail_url):
    # Extracts the barcode number from the thumbnail URL.
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


def scrape_missing_details(product_url, driver):
    #Scrape missing details from the product page using Selenium.
    driver.get(product_url)
    time.sleep(2)  # Allow time for the page to load

    try:
        name = driver.find_element(By.CSS_SELECTOR, "#pdp_product-title").text.strip()
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

    return name, description, brand, category, price_per_unit, weight_info, delivery_methods


def fetch_products(category_name, category_slug, driver):
    #Fetch all products from the category.
    page = 1
    all_products = []

    while True:
        url = f"{BASE_URL}{category_slug}.json"
        print(f"Fetching {category_name} from {url}...")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            break

        data = response.json()
        products_data = data.get("pageProps", {}).get("productCategory", {}).get("products_summary", {}).get("products", [])

        if not products_data:
            break

        # all_products = []
        for product in products_data:
            thumbnail_url = product.get("thumbnail_image", "N/A")
            barcode = extract_barcode(thumbnail_url)
            product_url = f'https://www.bigc.co.th/en/product/{product.get("slug", "")}'

            # Extract missing details
            name, description, brand, category, price_per_unit, weight_info, delivery_methods = scrape_missing_details(
                product_url, driver)

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

    return all_products


def main():
    all_data = []
    driver = setup_driver()

    for category_name, category_slug in CATEGORIES.items():
        category_products = fetch_products(category_name, category_slug, driver)
        all_data.extend(category_products)
        time.sleep(REQUEST_DELAY)

    driver.quit()

    # Save to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    total_products = get_total_products(category_slug)
    print(f"Total products in {category_slug}: {total_products}")
    print(f"Scraped {len(all_data)} total products!")


if __name__ == "__main__":
    main()
