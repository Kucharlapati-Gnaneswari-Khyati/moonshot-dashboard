from playwright.sync_api import sync_playwright
import pandas as pd
import re

def extract_size_from_title(title):
    title_lower = str(title).lower()
    if any(word in title_lower for word in ['cabin', 'small', '55cm', '55 cm', '55', '20 inch']): return 'Cabin'
    elif any(word in title_lower for word in ['medium', '65cm', '65 cm', '65', '24 inch']): return 'Medium'
    elif any(word in title_lower for word in ['large', '75cm', '75 cm', '75', '80cm', '28 inch']): return 'Large'
    return 'Medium'

print("Starting Ultra-Resilient Playwright Product Scraper...")

brands = [
    "Safari luggage", "Skybags luggage", "American Tourister luggage", 
    "VIP luggage", "Nasher Miles luggage", "Aristocrat luggage"
]

data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # Added a standard viewport so Amazon doesn't serve a weird mobile layout
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    for brand in brands:
        print(f"\nScraping brand: {brand}")
        search_url = f"https://www.amazon.in/s?k={brand.replace(' ', '+')}"
        
        try:
            page.goto(search_url, timeout=60000)
            # Scroll to load all elements
            page.evaluate("window.scrollBy(0, 2000)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollBy(0, 2000)")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"Failed to load page for {brand}. Error: {e}")
            continue

        products = page.query_selector_all('div[data-component-type="s-search-result"]')
        print(f"Products found on page: {len(products)}")

        saved_count = 0
        for product in products[:15]: # Grabs top 15 per brand
            try:
                # 1. Resilient Title
                title_tag = product.query_selector("h2") or product.query_selector(".a-text-normal")
                title = title_tag.text_content().strip() if title_tag else "N/A"

                # 2. Resilient Link (Tries h2 link, then general link)
                link_tag = product.query_selector("h2 a") or product.query_selector("a.a-link-normal.s-no-outline")
                link = "https://www.amazon.in" + link_tag.get_attribute("href") if link_tag else "N/A"

                # 3. Resilient Price
                price_tag = product.query_selector(".a-price-whole")
                price_str = price_tag.text_content() if price_tag else "0"
                price_clean = re.sub(r'[^\d]', '', price_str)
                price = int(price_clean) if price_clean else 0

                # DEBUG LOGGING: Tells us exactly what failed
                if link == "N/A" or price == 0:
                    print(f"  [Skipped] Reason -> Has Link: {link != 'N/A'} | Has Price: {price > 0} | Title: {title[:30]}...")
                    continue

                size = extract_size_from_title(title)

                # 5. List Price
                list_price_tag = product.query_selector("span.a-price.a-text-price span.a-offscreen")
                list_price_str = list_price_tag.text_content() if list_price_tag else str(price)
                list_price_clean = re.sub(r'[^\d]', '', list_price_str)
                list_price = int(list_price_clean) if list_price_clean else price
                
                discount = round(((list_price - price) / list_price) * 100, 2) if list_price > 0 else 0

                # 6. Rating & Reviews
                rating_tag = product.query_selector("span.a-icon-alt")
                rating = float(rating_tag.text_content().split(" ")[0]) if rating_tag else 0.0
                
                rev_count_tag = product.query_selector("span.a-size-base.s-underline-text")
                rev_str = rev_count_tag.text_content() if rev_count_tag else "0"
                rev_clean = re.sub(r'[^\d]', '', rev_str)
                review_count = int(rev_clean) if rev_clean else 0

                data.append({
                    "Brand": brand.replace(" luggage", "").title(),
                    "Title": title,
                    "Size": size,
                    "Price": price,
                    "List Price": list_price,
                    "Discount %": discount,
                    "Rating": rating,
                    "Review Count": review_count,
                    "Link": link
                })
                saved_count += 1

            except Exception as e:
                print(f"  [Error] parsing a product: {e}")
                continue
        
        print(f"Successfully extracted {saved_count} valid products for {brand}.")

    browser.close()

df = pd.DataFrame(data)

if len(df) > 0:
    df.to_csv("dataset.csv", index=False)
    df.to_csv("final_dataset.csv", index=False)
    print(f"\n✅ Scraping complete! {len(df)} products saved with valid links.")
else:
    print("\n❌ Error: No products were saved.")