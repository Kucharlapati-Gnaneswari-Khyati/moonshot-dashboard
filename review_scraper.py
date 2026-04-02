from playwright.sync_api import sync_playwright
import pandas as pd
import time

print("Loading dataset...")
df = pd.read_csv("final_dataset.csv") 

reviews_data = []

with sync_playwright() as p:
    # headless=False opens a visible browser so you can solve captchas if Amazon asks
    browser = p.chromium.launch(headless=False) 
    
    # Adding a realistic User-Agent to bypass basic bot detection
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for index, row in df.iterrows():
        link = row["Link"]
        brand = row["Brand"]
        title = row["Title"]
        
        # Skip empty or broken links
        if pd.isna(link) or link == "N/A":
            continue
            
        try:
            print(f"Scraping reviews for: {title[:40]}...")
            page.goto(link, timeout=60000)
            
            # Amazon lazy-loads reviews. We must scroll down to make them appear.
            page.evaluate("window.scrollBy(0, 3000)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollBy(0, 3000)")
            page.wait_for_timeout(3000) # Give it a moment to render

            # Grab the specific review blocks
            reviews = page.query_selector_all('div[data-hook="review"]')
            
            count = 0
            for review in reviews:
                if count >= 10: # Grab up to 10 reviews per product to hit your 300 target fast
                    break
                    
                text_elem = review.query_selector('span[data-hook="review-body"]')
                if text_elem:
                    review_text = text_elem.inner_text().strip()
                    if review_text:
                        reviews_data.append({
                            "Brand": brand,
                            "Product": title,
                            "Review": review_text
                        })
                        count += 1
                        
            print(f" -> Found {count} reviews")

        except Exception as e:
            print(f" -> Failed to extract: {e}")
            continue

    browser.close()

reviews_df = pd.DataFrame(reviews_data)
print(f"\n✅ Total reviews successfully extracted: {len(reviews_df)}")
reviews_df.to_csv("reviews.csv", index=False)
